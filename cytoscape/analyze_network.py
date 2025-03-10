import py4cytoscape as py4  # type: ignore
import pandas as pd  # type: ignore
from utils import (
    export_analysis_to_csv,
    pandas_degree,
    reset_filter,
    get_unique_filename,
)

# Ottieni l'elenco di tutte le reti nel progetto
# network_list = [
#     "snapshot_2019.graphml",
#     "snapshot_2020.graphml",
#     "snapshot_2021.graphml",
#     "snapshot_2022.graphml",
#     "snapshot_2023.graphml",
#     "snapshot_2024.graphml",
#     "snapshot_2025.graphml",
# ]
# network_list = ["snapshot_2025.graphml"]
network_list = ["random_graph.graphml"]

# Crea una lista per raccogliere i risultati
analysis_results = []

top = 100
min_degree = 2
# max_degree = 100000

# Itera su ogni rete
for network_name in network_list:
    # Imposta la rete corrente
    py4.set_current_network(network_name)

    print(f"Grafo selezionato: {network_name}")

    # py4.tools.analyze_network(directed=False)

    nodes_with_degrees = pandas_degree()
    max_degree = nodes_with_degrees[top][1] if len(nodes_with_degrees) > top else nodes_with_degrees[-1][1]

    initial_node_count = py4.get_node_count()
    initial_edge_count = py4.get_edge_count()

    # Crea un filtro per selezionare nodi con grado maggiore di 2 e minore o uguale al grado del decimo nodo
    filter_name = f"DegreeBetween{min_degree}And{max_degree}"
    criterion = [
        min_degree,
        max_degree,
    ]  # Seleziona nodi con grado tra 2 e il grado del decimo nodo
    py4.filters.create_degree_filter(
        filter_name,
        criterion,
        predicate="BETWEEN",
        edge_type="ANY",
        hide=False,
        apply=True,
    )

    # Ottieni la lista dei nodi selezionati
    selected_nodes = py4.get_selected_nodes(node_suids=True, network=network_name)
    reset_filter()

    if not selected_nodes:
        print(
            f"Nessun nodo soddisfa il criterio di selezione nella rete {network_name}."
        )
    else:
        # Nome del subnetwork da creare
        subnetwork_name = (
            f"Subnetwork_Degree_Between_{min_degree}_and_{max_degree}_{network_name}"
        )

        # Ottieni la lista delle reti esistenti
        existing_networks = py4.get_network_list()

        if subnetwork_name in existing_networks:
            print(
                f"Il subnetwork '{subnetwork_name}' esiste già. Uso quello esistente."
            )
            subnetwork_suid = py4.get_network_suid(
                subnetwork_name
            )  # Ottieni il SUID della rete esistente
        else:
            print(f"Creo il subnetwork '{subnetwork_name}'.")
            subnetwork_suid = py4.create_subnetwork(
                nodes=selected_nodes,
                subnetwork_name=subnetwork_name,
                network=network_name,
            )

        # Imposta la sottorete come rete corrente
        py4.set_current_network(subnetwork_suid)

        print(f"Analizzo la rete {network_name}")

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
        results["% Nodes"] = int(results["nodeCount"]) / initial_node_count
        results["% Channels"] = int(results["edgeCount"]) / initial_edge_count
        results["Max Degree"] = subnetwork_df["Degree"].max()

        # rimuovi la colonna time dal result
        results.pop("time", None)
        results.pop("networkTitle", None)

        # Aggiungi i risultati all'elenco
        analysis_results.append({"network": network_name, **results})

        # # Elimina la sottorete
        # py4.delete_network(subnetwork_suid)

        print(f"Rete {network_name} analizzata.")

export_analysis_to_csv(analysis_results)
