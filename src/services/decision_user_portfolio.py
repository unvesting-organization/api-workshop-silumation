from src.models.transaction import Transaction
from datetime import  datetime

def update_portfolio(name, portfolio, date, choices):
    # Define the investment logic
    selected_companies = [choice for choice in choices if choice not in ['Ninguna', 'Freeze', '']]

    # Determine actions
    actions = {}
    for company in portfolio['holdings'].keys():
        if company not in selected_companies:
            actions[company] = 'sell'
        else:
            actions[company] = 'hold'

    for company in selected_companies:
        if company not in portfolio['holdings']:
            actions[company] = 'buy'

    return [ Transaction(datetime.strptime(date, "%d/%m/%Y %H:%M:%S"), name, company, action) for company, action in actions.items()]