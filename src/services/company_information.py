import os
import pandas as pd


async def companies_data(key, time):
    if time == 0:
        sheet_id = os.getenv("CHANGES_COMPANY_SHARES_DATA")
        users_responses = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=766765566")
        current_data = users_responses.to_dict(orient='records')
    else:
        from src.utils.mongo_utils import MongoUtils
        current_docs = await MongoUtils.find_document(f"{key}_company_{time}", {})
        current_data = [{k: v for k, v in doc.items() if k != '_id'} for doc in current_docs]

        # Obtener los datos para el tiempo anterior
        if time == 1:
            sheet_id = os.getenv("CHANGES_COMPANY_SHARES_DATA")
            users_responses = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=766765566")
            previous_data = { doc['Nombre']: doc['Valor'] for doc in users_responses.to_dict(orient='records')}
            users_responses = { doc['Nombre']: doc['Image'] for doc in users_responses.to_dict(orient='records')}
        else:
            previous_docs = await MongoUtils.find_document(f"{key}_company_{time-1}", {})
            previous_data = {doc['Nombre']: doc['Valor'] for doc in previous_docs if 'Nombre' in doc and 'Valor' in doc}
            users_responses = { doc['Nombre']: doc['Image'] for doc in previous_docs}

        # Calcular el cambio porcentual y añadirlo a la lista de datos actuales
        for company in current_data:
            previous_value = previous_data.get(company['Nombre'], None)
            if previous_value:
                current_value = company['Valor']
                # Calcular el cambio porcentual
                change_percentage = ((current_value - previous_value) / previous_value) * 100
                company['Valor'] = round(company['Valor'],2)
                company['Cambio'] = round(change_percentage,2)
                company['Image'] = users_responses[company['Nombre']]
            else:
                company['Cambio'] = None  # En caso de no encontrar valor anterior, se asigna None
    return current_data

    