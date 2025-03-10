import py4cytoscape as py4  # type: ignore
import pandas as pd  # type: ignore
from utils import (
    export_analysis_to_csv,
    pandas_degree,
    reset_filter,
    get_unique_filename,
)

network_name = "random_graph.graphml"
analysis_results = []


py4.set_current_network(network_name)


# Esegui l'analisi della rete sulla sottorete
results = py4.tools.analyze_network(directed=False)

# Ottieni la tabella dei nodi della sottorete
subnetwork_node_table = py4.get_table_columns("node")
subnetwork_df = pd.DataFrame(subnetwork_node_table)

# Assicurati che la colonna 'Degree' sia numerica e calcola la mediana
subnetwork_df["Degree"] = pd.to_numeric(
    subnetwork_df["Degree"], errors="coerce"
)

results["Med Degree"] = subnetwork_df["Degree"].median()
results["Avg Degree"] = subnetwork_df["Degree"].mean()

# rapporto archi/nodi
results["C/N"] = int(results["edgeCount"]) / int(results["nodeCount"])
# results["% Nodes"] = int(results["nodeCount"]) / initial_node_count
# results["% Channels"] = int(results["edgeCount"]) / initial_edge_count
results["Max Degree"] = subnetwork_df["Degree"].max()

# min_degree
# print(f"min_degree: {subnetwork_df['Degree'].min()}")

# rimuovi la colonna time dal result
results.pop("time", None)
results.pop("networkTitle", None)

# Aggiungi i risultati all'elenco
analysis_results.append({"network": network_name, **results})

# # Elimina la sottorete
# py4.delete_network(subnetwork_suid)

print(f"Rete {network_name} analizzata.")

export_analysis_to_csv(analysis_results)