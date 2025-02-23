import csv
import os
import py4cytoscape as py4  # type: ignore
import pandas as pd  # type: ignore


def reset_filter():
    # Creiamo un filtro che include tutti i nodi (DEGREE ≥ 0)
    py4.filters.create_degree_filter(
        "Reset_Filter",  # Nome filtro
        criterion=[0, 100000],  # Tutti i nodi hanno grado ≥ 0
        predicate="BETWEEN",  # Sempre vero
        edge_type="ANY",
        hide=False,  # Non nasconde nulla
        apply=True,  # Applica il filtro
    )


# Funzione per generare un nome di file univoco
def get_unique_filename(base_name, extension):
    counter = 1
    while os.path.exists(f"{base_name}_{counter}{extension}"):
        counter += 1
    return f"{base_name}_{counter}{extension}"


def pandas_degree():
    # Ottieni la tabella dei nodi
    node_table = py4.get_table_columns("node")

    # Converte la tabella in un DataFrame pandas
    df = pd.DataFrame(node_table)

    # Assicurati che la colonna 'Degree' sia numerica
    df["Degree"] = pd.to_numeric(df["Degree"], errors="coerce")

    # Rimuove eventuali valori NaN nella colonna 'Degree'
    df = df.dropna(subset=["Degree"])

    # Crea una lista di tuple (node_suid, degree)
    nodes_with_degrees = [
        (pub_key, degree) for pub_key, degree in zip(df["pub_key"], df["Degree"])
    ]

    # Ordina i nodi per grado in ordine decrescente
    nodes_with_degrees.sort(key=lambda x: x[1], reverse=True)

    return nodes_with_degrees


# Esporta i risultati in un file CSV
def export_analysis_to_csv(analysis_results):
    csv_filename = get_unique_filename("network_analysis_results", ".csv")

    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=analysis_results[0].keys(), delimiter="\t"
        )
        writer.writeheader()
        for result in analysis_results:
            for key in result:
                if isinstance(result[key], float):
                    result[key] = str(result[key]).replace(
                        ".", ","
                    )  # Sostituisce . con ,
            writer.writerow(result)

    print(f"Risultati esportati in {csv_filename}.")  # Stampa il nome del file
