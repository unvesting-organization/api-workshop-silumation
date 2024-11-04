from dataclasses import dataclass
from typing import List, Dict
from collections import defaultdict

@dataclass
class UserPortfolio:
    bought: Dict[str, List[Dict[str, float]]]  # stock_symbol -> list of {'quantity': int, 'price': float}
    sold: Dict[str, List[Dict[str, float]]]    # stock_symbol -> list of {'quantity': int, 'price': float}

    def __init__(self):
        self.bought = defaultdict(list)
        self.sold = defaultdict(list)