# src/services/data_processing.py
import os
import pandas as pd
import csv

market_factors_df = pd.read_csv("src/docs/market_factors.csv")
market_base_df = {fila['name']: float(fila['cost']) for fila in csv.DictReader(open("src/docs/market_base.csv", encoding='utf-8'))}

def process_decision(decision: str, moment: int):
    final = {}
    if moment == 1:
        final[decision["Nombre Usuario"]] = {
            "monto" : 1000
        } 
        if decision["Empresa a Invertir"] == None or decision["Empresa 2 a Invertir"] == None:
            empresa_name = decision["Empresa a Invertir"] if decision["Empresa a Invertir"] != None else decision["Empresa 2 a Invertir"]
            final[decision["Nombre Usuario"]][1] = {
                empresa_name : 1000/market_base_df[empresa_name]["cost"]
            }
        else:
            final[decision["Nombre Usuario"]][1] = {
                decision["Empresa a Invertir"] : 500/market_base_df[decision["Empresa a Invertir"]],
                decision["Empresa 2 a Invertir"] : 500/market_base_df[decision["Empresa 2 a Invertir"]]
            }
    else:
        pass

    return final


def retrieve_and_process_data(key: str, time: int):
    try:
        sheet_id = "1yurPkKC-0LugxxS11mmXOP6fRp0ceVZ5LvwzqzQ79m0"

        df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
        df = df[(df["Contraseña"] == key) & (df["Momento"] <= time)]
        return [process_decision(row, time) for _, row in df.iterrows()]
        
    except Exception as e:
        print(e)
        return None