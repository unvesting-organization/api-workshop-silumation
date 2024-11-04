import os
import pandas as pd

def companies_data(time):
    sheet_id = os.getenv("CHANGES_COMPANY_SHARES_DATA")
    users_responses = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=766765566")
    rows_to_return = time * 4
    users_responses = users_responses.head(rows_to_return)

    data_list = users_responses.to_dict(orient='records')
    return data_list

    