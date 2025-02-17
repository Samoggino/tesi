# export.py
import networkx as nx
import os
from utils import convert_attributes
import json


# Funzione per esportare il grafo in formato GraphML
def export_graph_to_graphml(filtered_nodes_data, filtered_channels, graphml_file):
    # Crea un grafo vuoto
    G = nx.Graph()

    # Aggiungi i nodi al grafo
    for node in filtered_nodes_data:
        node_attributes = convert_attributes(node)
        G.add_node(node["pub_key"], **node_attributes)

    # Aggiungi gli archi (canali) al grafo
    for edge in filtered_channels:
        edge_attributes = convert_attributes(edge)
        G.add_edge(edge["node1_pub"], edge["node2_pub"], **edge_attributes)

    # if os.path.exists(graphml_file):
    #     print(f"Il file {graphml_file} esiste già. Non verrà sovrascritto.")
    # else:
    print(f"Nodi totali: {G.number_of_nodes()}")
    print(f"Archi totali: {G.number_of_edges()}")
    nx.write_graphml(G, graphml_file)
    print(f"Graph exported to '{graphml_file}'")


def export_graph_to_json(filtered_nodes_data, filtered_channels, json_file):
    # Costruzione del dizionario
    data = {"nodes": filtered_nodes_data, "edges": filtered_channels}

    # if os.path.exists(json_file):
    #     print(f"Il file {json_file} esiste già. Non verrà sovrascritto.")
    # else:
    #     # Salva il JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
