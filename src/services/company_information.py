import os
import pandas as pd


async def companies_data(key, time):
    if time == 0:
        sheet_id = os.getenv("CHANGES_COMPANY_SHARES_DATA")
        users_responses = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=766765566")
        data_list = users_responses.to_dict(orient='records')
    else:
        from src.utils.mongo_utils import MongoUtils
        documentos = await MongoUtils.find_document(f"{key}_company_{time}", {})
        data_list = [{k: v for k, v in doc.items() if k != '_id'} for doc in documentos]
    return data_list

    