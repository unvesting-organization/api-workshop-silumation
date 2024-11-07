from typing import List, Dict
from src.models.participant_portfolio import UserPortfolio


def rank_users(user_portfolios: Dict[str, UserPortfolio], current_prices: Dict[str, float]) -> List[Dict]:
    """
    Ranks users based on their net worth (balance + value of holdings at current prices).
    Returns a list of dictionaries containing user information.
    """
    user_rankings = []
    for user_id, portfolio in user_portfolios.items():
        holdings_value = sum(
            portfolio.holdings.get(stock, 0) * current_prices.get(stock, 0)
            for stock in portfolio.holdings
        )
        net_worth = (portfolio.balance + holdings_value)/10
        companies_invested = list(portfolio.holdings.keys())
        user_info = {
            'user_id': user_id,
            'companies': companies_invested,
            'net_worth': net_worth
        }
        user_rankings.append(user_info)
    # Sort users by net worth in descending order
    user_rankings.sort(key=lambda x: x['net_worth'], reverse=True)
    return user_rankings
