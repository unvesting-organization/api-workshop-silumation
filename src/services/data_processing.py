import pandas as pd
import os
from src.services.decision_user_portfolio import update_portfolio
from src.services.company_information import companies_data
from src.services.simulate_broker import simulate_broker
from src.services.rank_users import rank_users

def retrieve_and_process_data(password: str, time: int):
    try:
        market_base = companies_data(time)

        # Define user responses
        sheet_id = os.getenv("USER_DECISIONS_DATA")
        if not os.path.exists(f'{password}.csv'):
            pd.DataFrame(market_base)[['Nombre', 'Valor']].to_csv(f'{password}.csv', index=False)
        # Convert the file to a pandas dataframe
        current_prices = pd.read_csv(f'{password}.csv')
            
        users_responses = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
        users_responses = users_responses[(users_responses["Contraseña"] == password) & (users_responses["Momento"] <= time)]
        users_responses.dropna()
        users_responses.sort_values(by=['Nombre Usuario', 'Momento'], inplace=True)

        transactions = []
        for user in users_responses['Nombre Usuario'].unique():
            user_data = users_responses[users_responses['Nombre Usuario'] == user].sort_values(by='Momento')
            portfolio = {'cash': 1000, 'holdings': {}, 'history': {}}

            for idx, row in user_data.iterrows():
                date = row['Marca temporal']
                choices = [row['Empresa a Invertir'], row['Empresa 2 a Invertir']]

                # Update holdings based on choices
                portfolio = update_portfolio(user, portfolio, date, choices)
                transactions += portfolio
        
        if not os.path.exists(f'{password}_participants.csv'):
            pd.DataFrame(transactions).to_csv(f'{password}_participants.csv', index=False)
        
        market_base = { company["Nombre"] : company["Valor"] for company in market_base}
        current_prices, portafolios = simulate_broker(transactions, market_base)
        return rank_users(portafolios, current_prices)
    except Exception as e:
        raise e
