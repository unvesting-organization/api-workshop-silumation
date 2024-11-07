import pandas as pd
import os
from src.services.decision_user_portfolio import update_portfolio
from src.services.company_information import companies_data
from src.services.simulate_broker import simulate_broker
from src.services.rank_users import rank_users
from src.utils.mongo_utils import MongoUtils
from src.utils.merge_portfolio import merge_portfolios
from src.services.changes_company_shares import changes_shares

async def retrieve_and_process_data(password: str, time: int):
    try:
        market_base = await companies_data(password, time-1)
        changes_shares_values = { company["Nombre"] : company["Cambio"] for company in changes_shares(time-1)}
        # Define user responses
        sheet_id = os.getenv("USER_DECISIONS_DATA")
        await MongoUtils.create_collection(f"{password}_portfolios_{time}")
        await MongoUtils.create_collection(f"{password}_company_{time}")

        current_prices = [{'Nombre': item['Nombre'], 'Valor': item['Valor']} for item in market_base]
            
        users_responses = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
        users_responses = users_responses[(users_responses["Contraseña"] == password) & (users_responses["Momento"] == time)]
        # Filter to keep only the oldest entry per user based on 'Marca temporal'
        users_responses = users_responses.loc[users_responses.groupby('Nombre Usuario')['Marca temporal'].idxmin()]
        portafolios = await MongoUtils.find_document(f"{password}_portfolios_{time-1}", {}) if time > 1 else [{'user_id': user , 'holdings': {}, 'history': {}} for user in users_responses['Nombre Usuario'].unique()]

        users_responses.dropna()
        users_responses.sort_values(by=['Nombre Usuario', 'Momento'], inplace=True)

        transactions = []
        for user in users_responses['Nombre Usuario'].unique():
            user_data = users_responses[users_responses['Nombre Usuario'] == user].sort_values(by='Momento')
            portfolio = next((dic for dic in portafolios if dic['user_id'] == user), {'user_id': user , 'holdings': {}, 'history': {}})

            for idx, row in user_data.iterrows():
                date = row['Marca temporal']
                if time == 1:
                    choices = [row['Invierte en una empresa'], "Ninguna"]
                else:
                    choices = [row['Empresa a Invertir'], row['Empresa 2 a Invertir']]

                # Update holdings based on choices
                portfolio = update_portfolio(user, portfolio, date, choices)
                transactions += portfolio
        
        market_base_lite = { company["Nombre"] : company["Valor"] + changes_shares_values[company["Nombre"]] for company in market_base}

        current_prices, portafolios_update = simulate_broker(transactions, market_base_lite)
        changes_shares_values = { company["Nombre"] : company["Cambio"] for company in changes_shares(time)}
        current_prices =  { name : value + changes_shares_values[name] for name, value in current_prices.items()}
        await MongoUtils.insert_many_portfolios(f"{password}_portfolios_{time}", portafolios_update)

        ranking = rank_users(portafolios, current_prices)
        #print
        merged = [{**empresa, 'Valor': current_prices[empresa['Nombre']]} for empresa in market_base]
        await MongoUtils.insert_many_companies(f"{password}_company_{time}", merged, "Valor")
        return ranking
    except Exception as e:
        raise e
    finally:
        await MongoUtils.close_connection()
