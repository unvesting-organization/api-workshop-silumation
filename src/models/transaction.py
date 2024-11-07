from dataclasses import dataclass
import datetime

@dataclass
class Transaction:
    date: datetime.date
    user_id: str
    stock_symbol: str
    type: str  # 'buy', 'sell', 'hold'

def update_price(current_price: float, transaction_type: str, quantity: int,
                buy_factor: float = 0.5, sell_factor: float = 0.4) -> float:
    """
    Actualiza el precio de la acción basado en el tipo de transacción.
    """
    if transaction_type == 'buy':
        current_price += ((buy_factor * quantity)/((500-quantity)/current_price))
    elif transaction_type == 'sell':
        current_price -= ((sell_factor * quantity)/((500-quantity)/current_price))
    # 'hold' no cambia el precio
    return max(current_price, 0)  # Evita precios negativos