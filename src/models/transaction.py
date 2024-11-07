from dataclasses import dataclass
import datetime

@dataclass
class Transaction:
    date: datetime.date
    user_id: str
    stock_symbol: str
    type: str  # 'buy', 'sell', 'hold'

def update_price(current_price: float, transaction_type: str, quantity: int,
                buy_factor: float = 0.5, sell_factor: float = 0.8) -> float:
    """
    Actualiza el precio de la acción basado en el tipo de transacción.
    """
    if transaction_type == 'buy':
        current_price += (current_price * quantity * buy_factor)/1500
    elif transaction_type == 'sell':
        current_price -= (current_price * quantity * sell_factor)/1500
    # 'hold' no cambia el precio
    return max(current_price, 0)  # Evita precios negativos