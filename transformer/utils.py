# utils.py
import json
from datetime import datetime


# Funzione per convertire last_update in formato ISO 8601
def convert_last_update_iso(last_update):
    return (
        datetime.utcfromtimestamp(last_update).isoformat() if last_update > 0 else None
    )


# Funzione per convertire gli attributi in formati supportati da NetworkX
def convert_attributes(attributes):
    converted = {}
    for k, v in attributes.items():
        if v is None:
            # Gestisce i valori None assegnando una stringa vuota o un valore predefinito
            converted[k] = ""
        elif isinstance(v, list) or isinstance(v, dict):
            # Converte liste e dizionari in stringhe JSON
            converted[k] = json.dumps(v)
        elif (
            k == "capacity" and v.isdigit()
        ):  # Verifica se "capacity" è una stringa numerica
            converted[k] = float(v)  # Converte capacity in float
        else:
            converted[k] = v
    return converted
