from dataclasses import dataclass
import datetime

@dataclass
class Transaction:
    date: datetime.date
    user_id: str
    stock_symbol: str
    type: str  # 'buy', 'sell', 'hold'

def update_price(current_price: float, transaction_type: str, quantity: int,
                buy_factor: float = 0.01, sell_factor: float = 0.01) -> float:
    """
    Updates the stock price based on the transaction type.
    
    :param current_price: Current price of the stock.
    :param transaction_type: Type of transaction ('buy', 'sell', 'hold').
    :param quantity: Number of shares transacted.
    :param buy_factor: Percentage increase per share bought.
    :param sell_factor: Percentage decrease per share sold.
    :return: Updated price of the stock.
    """
    if transaction_type == 'buy':
        current_price += current_price * buy_factor * quantity
    elif transaction_type == 'sell':
        current_price -= current_price * sell_factor * quantity
    # 'hold' does not change the price
    return max(current_price, 0)  # Ensure price doesn't go negative