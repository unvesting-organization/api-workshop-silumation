from dataclasses import dataclass, field
from typing import Dict
from collections import defaultdict

@dataclass
class UserPortfolio:
    balance: float
    holdings: Dict[str, int] = field(default_factory=lambda: defaultdict(int))