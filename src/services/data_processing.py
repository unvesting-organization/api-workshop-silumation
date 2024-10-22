# src/services/data_processing.py
import os
import pandas as pd

def retrieve_and_process_data(key: str, time: int):
    sheet_id = "1yurPkKC-0LugxxS11mmXOP6fRp0ceVZ5LvwzqzQ79m0"

    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

    print(df)