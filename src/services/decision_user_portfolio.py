def update_portfolio(portfolio, choices, current_prices):
    # Define the investment logic
    selected_companies = [choice for choice in choices if choice not in ['Ninguna', 'Freeze', '']]
    num_selected = len(selected_companies)

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

    # Execute actions
    # Sell
    for company, action in actions.items():
        if action == 'sell':
            shares = portfolio['holdings'].pop(company, 0)
            next_price = current_prices[company]
            portfolio['cash'] += shares * next_price

    # Buy
    aux = sum([1 for action in actions.values() if action == 'sell'])
    if num_selected > 0 and aux < num_selected:
        invest_per_company = portfolio['cash'] / (num_selected-aux)
        portfolio['cash'] = 0
        for company in selected_companies:
            if actions.get(company) == 'buy':
                price = current_prices[company]
                shares = invest_per_company / price
                portfolio['holdings'][company] = shares
            elif actions.get(company) == 'hold':
                pass  # Do nothing, already holding the shares
    return portfolio