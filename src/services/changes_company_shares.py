import os
import pandas as pd

def changes_shares(time):
    try:
        sheet_id = os.getenv("CHANGES_COMPANY_SHARES_DATA")
        users_responses = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")
        users_responses.fillna('', inplace=True)
        users_responses = users_responses[users_responses["Momento"] == time]

        data_list = users_responses[["Nombre", "Cambio"]].to_dict(orient='records')
        return data_list
    except Exception as e:
        print("Failed in changes_shares")
        raise e