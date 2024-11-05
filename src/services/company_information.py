import os
import pandas as pd

def companies_data():
    sheet_id = os.getenv("CHANGES_COMPANY_SHARES_DATA")
    users_responses = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=766765566")

    data_list = users_responses.to_dict(orient='records')
    return data_list

    