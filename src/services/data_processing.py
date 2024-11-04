import pandas as pd
import os
from src.services.decision_user_portfolio import update_portfolio

def retrieve_and_process_data(password: str, time: int):
    try:
        market_base = pd.read_csv("src/docs/market_base.csv")
        market_base.set_index('name', inplace=True)

        market_factors = pd.read_csv("src/docs/market_factors.csv")

        # Compute company prices over time
        companies = market_base.index.tolist()
        times = sorted(market_factors['time'].unique())
        price_history = pd.DataFrame(index=times, columns=companies)

        for company in companies:
            base_price = market_base.loc[company, 'cost']
            price = base_price
            price_history.loc[0, company] = base_price
            factors = market_factors[market_factors['company'] == company].set_index('time').sort_index()
            for time in times:
                change_pct = factors.loc[time, 'change'] 
                price += change_pct
                price_history.loc[time, company] = round(price, 2)

        # Define user responses
        sheet_id = os.getenv("USER_DECISIONS_DATA")

        users_responses = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
        users_responses = users_responses[(users_responses["Contraseña"] == password) & (users_responses["Momento"] <= time)]
        users_responses.fillna('', inplace=True)
        users_responses.sort_values(by=['Nombre Usuario', 'Momento'], inplace=True)

        # Process each user's investments
        initial_capital = 1000
        user_portfolios = {}

        for user in users_responses['Nombre Usuario'].unique():
            user_data = users_responses[users_responses['Nombre Usuario'] == user].sort_values(by='Momento')
            portfolio = {'cash': initial_capital, 'holdings': {}, 'history': {}}

            for idx, row in user_data.iterrows():
                moment = row['Momento']
                choices = [row['Empresa a Invertir'], row['Empresa 2 a Invertir']]
                choices = [choice if choice != '' else 'Ninguna' for choice in choices]
                time = int(moment)

                # Update holdings based on choices
                portfolio = update_portfolio(portfolio, choices, price_history.loc[time-1])

                # Record portfolio value
                total_value = portfolio['cash']
                for company, shares in portfolio['holdings'].items():
                    total_value += shares * price_history.loc[time + 1, company]
                portfolio['history'][moment] = total_value

            user_portfolios[user] = portfolio

        return user_portfolios
    except Exception as e:
        print(e)
        raise e
