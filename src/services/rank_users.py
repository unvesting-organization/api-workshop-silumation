from typing import List, Dict

def rank_users(user_portfolios: Dict[str, Dict], current_prices: Dict[str, float]) -> List[Dict]:
    """
    Ranks users based on their net worth (balance + value of holdings at current prices).
    Returns a list of dictionaries containing user information.
    """
    user_rankings = []
    for portfolio in user_portfolios:
        holdings_value = sum(
            quantity * current_prices.get(name, 0)
            for name, quantity in portfolio['holdings'].items()
        )
        money = holdings_value
        net_worth = ((money)/10)-100
        companies_invested = list(portfolio['holdings'].keys())
        user_info = {
            'user_id': portfolio["user_id"],
            'companies': companies_invested,
            'net_worth':round(net_worth,2),
            'balance': round(money,2),
        }
        user_rankings.append(user_info)
    # Sort users by net worth in descending order
    user_rankings.sort(key=lambda x: x['net_worth'], reverse=True)
    return user_rankings
