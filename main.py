# main.py
from filter import filter_graph
from export import export_graph_to_graphml
from datetime import datetime

# Nomi delle cartelle di input e output
input_folder = "json"  # Cartella di input
output_folder = "graphml"  # Cartella di output

# Nomi dei file
input_file_name = "lnd_1_graph_2025-02-06_00-00-21"
graphml_file_name = "prova"

# Costruisci i percorsi dei file
input_file = f"{input_folder}/{input_file_name}.json"
graphml_file = f"{output_folder}/{graphml_file_name}.graphml"

# Data dello snapshot (estratta dal nome del file)
snapshot_date = datetime.strptime("2025-02-06", "%Y-%m-%d")

# Filtra i dati
filtered_nodes_data, filtered_channels = filter_graph(input_file, snapshot_date)

# Esporta il grafo in formato GraphML
export_graph_to_graphml(filtered_nodes_data, filtered_channels, graphml_file)