from datetime import datetime

def convert_to_timestamp(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return int(dt.timestamp())
    except ValueError as e:
        return f"Errore: {e}"

# Inserisci direttamente la data qui Formato: YYYY-MM-DD
# date_input = "2022-08-23" # 2018

# date_input = "2019-01-01" # 2019-gen 1546297200

# date_input = "2019-11-01" # 2019-nov 1572562800

# date_input = "2020-10-14" # 2020

date_input = "2021-01-01" # 2021

# date_input = "2022-03-31" # 2022 1648677600 

# date_input = "2023-07-15" # 2023

print(date_input)
print(convert_to_timestamp(date_input))
