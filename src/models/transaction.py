from dataclasses import dataclass
import datetime

@dataclass
class Transaction:
    date: datetime.date
    user_id: str
    stock_symbol: str
    type: str  # 'buy', 'sell', 'hold'
    quantity: int