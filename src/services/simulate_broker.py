from dataclasses import dataclass, field
from typing import List, Dict
from collections import defaultdict
import datetime
from src.models.transaction import Transaction, update_price
from src.models.participant_portfolio import UserPortfolio

def simulate_broker(transactions: List[Transaction], base_prices: Dict[str, float],
                   initial_balance: float = 1000.0) -> (Dict[str, Dict[datetime.date, float]], Dict[str, UserPortfolio]): # type: ignore
    """
    Simula las operaciones del broker actualizando precios y gestionando portafolios de usuarios.
    """
    # Ordenar transacciones por fecha
    transactions.sort(key=lambda x: x.date)
    
    # Agrupar transacciones por fecha y símbolo de acción
    transactions_by_date_stock = defaultdict(lambda: defaultdict(list))
    for txn in transactions:
        transactions_by_date_stock[txn.date][txn.stock_symbol].append(txn)
    
    # Inicializar precios actuales con precios base
    current_prices = base_prices.copy()
    
    # Inicializar historial de precios
    price_history = {symbol: {} for symbol in base_prices}
    
    # Inicializar portafolios de usuarios con balance inicial
    user_portfolios = defaultdict(lambda: UserPortfolio(balance=initial_balance))
    
    # Simular cambios de precios y gestionar portafolios
    for date in sorted(transactions_by_date_stock.keys()):
        for stock, txns in transactions_by_date_stock[date].items():
            for txn in txns:
                user = user_portfolios[txn.user_id]
                if txn.type == 'buy':
                    user_txns = [t for t in txns if t.user_id == txn.user_id and t.type == 'buy']
                    num_buys = len(user_txns)
                    allocated_money = user.balance / num_buys if num_buys > 0 else 0
                    # Determinar cuántas acciones se pueden comprar con el dinero asignado
                    price_per_share = current_prices[stock]
                    shares_to_buy = int(allocated_money // price_per_share)
                    if shares_to_buy > 0:
                        total_cost = shares_to_buy * price_per_share
                        user.balance -= total_cost
                        user.holdings[stock] += shares_to_buy
                        # Actualizar el precio de la acción
                        current_prices[stock] = update_price(current_prices[stock], 'buy', shares_to_buy)
                        print(f"{txn.user_id} compró {shares_to_buy} acciones de {stock} a ${price_per_share:.2f} cada una, costo total: ${total_cost:.2f}")
                    else:
                        print(f"{txn.user_id} no pudo comprar acciones de {stock} por falta de fondos.")
                elif txn.type == 'sell':
                    # Vender todas las acciones que el usuario tiene de este stock
                    shares_to_sell = user.holdings.get(stock, 0)
                    if shares_to_sell > 0:
                        price_per_share = current_prices[stock]
                        total_revenue = shares_to_sell * price_per_share
                        user.balance += total_revenue
                        user.holdings[stock] = 0
                        # Actualizar el precio de la acción
                        current_prices[stock] = update_price(current_prices[stock], 'sell', shares_to_sell)
                        print(f"{txn.user_id} vendió {shares_to_sell} acciones de {stock} a ${price_per_share:.2f} cada una, ingresos totales: ${total_revenue:.2f}")
                    else:
                        print(f"{txn.user_id} no tiene acciones de {stock} para vender.")
                elif txn.type == 'hold':
                    # Mantener, no se realiza ninguna acción
                    print(f"{txn.user_id} mantiene su posición en {stock}.")
            # Registrar el precio actualizado después de todas las transacciones del día para este stock
            price_history[stock][date] = current_prices[stock]
    
    return price_history, user_portfolios

def rank_users(user_portfolios: Dict[str, UserPortfolio]) -> List[tuple]:
    """
    Genera un ranking de usuarios basado en su balance actual.
    """
    # Ordenar usuarios por balance en orden descendente
    ranked_users = sorted(user_portfolios.items(), key=lambda x: x[1].balance, reverse=True)
    return ranked_users

# # Ejemplo de Uso
# if __name__ == "__main__":
#     # Transacciones de ejemplo
#     transactions = [
#         Transaction(date=datetime.date(2024, 1, 10), user_id='User1', stock_symbol='AAPL', type='buy'),
#         Transaction(date=datetime.date(2024, 1, 10), user_id='User1', stock_symbol='GOOG', type='buy'),
#         Transaction(date=datetime.date(2024, 1, 15), user_id='User2', stock_symbol='GOOG', type='sell'),
#         Transaction(date=datetime.date(2024, 2, 5), user_id='User1', stock_symbol='AAPL', type='buy'),
#         Transaction(date=datetime.date(2024, 2, 20), user_id='User3', stock_symbol='MSFT', type='hold'),
#         Transaction(date=datetime.date(2024, 3, 10), user_id='User2', stock_symbol='AAPL', type='sell'),
#         Transaction(date=datetime.date(2024, 3, 15), user_id='User4', stock_symbol='GOOG', type='buy'),
#         # Agrega más transacciones según sea necesario
#     ]
      
#     # Precios base para cada acción
#     base_prices = {
#         'AAPL': 150.0,
#         'GOOG': 2800.0,
#         'MSFT': 300.0,
#         # Agrega más acciones según sea necesario
#     }
    
#     # Ejecutar la simulación
#     historial, portafolios = simulate_broker(transactions, base_prices)
    
#     # Imprimir historial de precios
#     print("\n=== Historial de Precios ===")
#     for stock, fechas in historial.items():
#         print(f"--- {stock} ---")
#         for fecha, precio in sorted(fechas.items()):
#             print(f"Fecha: {fecha}, Precio: ${precio:.2f}")
#         print()
    
#     # Generar y imprimir ranking de usuarios
#     ranking = rank_users(portafolios)
    
#     print("=== Ranking de Usuarios por Balance ===")
#     for rank, (user_id, portfolio) in enumerate(ranking, start=1):
#         print(f"{rank}. {user_id}: Balance de ${portfolio.balance:.2f}")
