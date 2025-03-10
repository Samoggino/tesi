import py4cytoscape as py4
import pandas as pd

# Ottieni la rete attiva
network_suid = py4.get_network_suid()

py4.set_current_network("random_graph.graphml")

# Controlla di nuovo le colonne
subnetwork_node_table = py4.get_table_columns("node")
subnetwork_df = pd.DataFrame(subnetwork_node_table)

# rimuovi la colonna 'Degree'
subnetwork_df = subnetwork_df.drop(columns=["Degree"])

print("Colonne disponibili dopo analyze_network:", subnetwork_df.columns.tolist())