import pandas as pd
import os
from src.services.decision_user_portfolio import update_portfolio
from src.services.company_information import companies_data
from src.services.simulate_broker import simulate_broker
from src.services.rank_users import rank_users
from src.utils.mongo_utils import MongoUtils

async def retrieve_and_process_data(password: str, time: int):
    try:
        market_base = await companies_data(password, time-1)

        # Define user responses
        sheet_id = os.getenv("USER_DECISIONS_DATA")

        await MongoUtils.create_collection(f"{password}_portfolios")
        await MongoUtils.create_collection(f"{password}_company_{time}")

        current_prices = [{'Nombre': item['Nombre'], 'Valor': item['Valor']} for item in market_base]
            
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
        
        market_base_lite = { company["Nombre"] : company["Valor"] for company in market_base}
        current_prices, portafolios = simulate_broker(transactions, market_base_lite)
        await MongoUtils.insert_many_portfolios(f"{password}_portfolios", portafolios)

        ranking = rank_users(portafolios, current_prices)
        merged = [{**empresa, 'Valor': current_prices[empresa['Nombre']]} for empresa in market_base]
        await MongoUtils.insert_many_companies(f"{password}_company_{time}", merged)
        return ranking
    except Exception as e:
        raise e
