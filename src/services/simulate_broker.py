from typing import List, Dict
from collections import defaultdict
import datetime
from src.models.transaction import Transaction, update_price
from src.models.participant_portfolio import UserPortfolio

def simulate_broker(transactions: List[Transaction], base_prices: Dict[str, float],
                   initial_balance: float = 800.0) -> (Dict[str, Dict[datetime.date, float]], Dict[str, UserPortfolio]): # type: ignore
    """
    Simula las operaciones del broker actualizando precios y gestionando portafolios de usuarios.
    """
    # Ordenar transacciones por fecha
    transactions.sort(key=lambda x: x.date)
    
    # Agrupar transacciones por fecha y símbolo de acción
    transactions_by_date_stock = defaultdict(list)
    for txn in transactions:
        transactions_by_date_stock[txn.date].append(txn)
    
    # Inicializar precios actuales con precios base
    current_prices = base_prices.copy()
    
    # Inicializar historial de precios
    price_history = {symbol: {} for symbol in base_prices}
    
    # Inicializar portafolios de usuarios con balance inicial
    user_portfolios = defaultdict(lambda: UserPortfolio(balance=initial_balance))
    
    # Simular cambios de precios y gestionar portafolios
    try:
        for date in sorted(transactions_by_date_stock.keys()):
            txns_internal = transactions_by_date_stock[date].copy()
            for txns in transactions_by_date_stock.values():
                for txn in transactions_by_date_stock[date]:
                    user = user_portfolios[txn.user_id]
                    user.balance += 100
                    stock = txn.stock_symbol
                    if txn.type == 'buy':
                        user_txns = [t for t in txns_internal if t.user_id == txn.user_id and t.type == 'buy']
                        num_buys = len(user_txns)
                        allocated_money = user.balance / num_buys if num_buys > 0 else 0
                        # Determinar cuántas acciones se pueden comprar con el dinero asignado
                        price_per_share = current_prices[stock]
                        shares_to_buy = float(allocated_money / price_per_share)
                        if shares_to_buy > 0:
                            total_cost = shares_to_buy * price_per_share
                            user.balance -= total_cost
                            user_portfolios[txn.user_id].holdings[stock] += shares_to_buy
                            txns_internal.remove(txn)
                            # Actualizar el precio de la acción
                            current_prices[stock] = update_price(current_prices[stock], 'buy', shares_to_buy)
                            print(f"{txn.user_id} compró {shares_to_buy} acciones de {stock} a ${price_per_share:.2f} cada una, costo total: ${total_cost:.2f}")
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
    except Exception as e:
        print(f"Error en la simulación: {e}")
    return current_prices, user_portfolios