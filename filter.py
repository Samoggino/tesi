import json
import networkx as nx
from numpy import double
from utils import convert_last_update_iso
from datetime import datetime, timedelta


def filter_graph(input_file, snapshot_date):
    # Calcolare la data limite (1 anno prima della data dello snapshot)
    one_year_ago = snapshot_date - timedelta(days=365)

    # Carica il JSON
    try:
        with open(input_file) as f:
            data = json.load(f)
            print("File JSON caricato con successo.")
    except json.decoder.JSONDecodeError as e:
        print(f"Errore nel caricare il file JSON: {e}")
        exit(1)

    # Creazione del grafo con NetworkX
    G = nx.Graph()

    # Mappa pub_key -> nodo per preservare tutti i dati originali
    node_map = {node["pub_key"]: node for node in data["nodes"]}

    # Aggiunta nodi al grafo, filtrando per last_update
    for node in data["nodes"]:
        last_update = node.get("last_update", 0)
        if (
            last_update > 0
            and one_year_ago <= datetime.utcfromtimestamp(last_update) <= snapshot_date
        ):
            G.add_node(node["pub_key"], last_update=last_update)

    # Aggiunta canali (archi) al grafo
    edge_list = []
    filtered = 0
    for edge in data["edges"]:
        if (
            int(edge["capacity"]) > 0
            and edge.get("node1_policy")
            and edge.get("node2_policy")
        ):
            G.add_edge(edge["node1_pub"], edge["node2_pub"])
            edge_list.append(edge)
        else:
            filtered += 1

    print(f"Canali filtrati: {filtered}")

    # **Fase 1: Rimuovere nodi con last_update == 0 e nodi isolati**
    removed = True
    while removed:
        removed = False
        nodes_to_remove = {
            n for n, attr in G.nodes(data=True) if attr.get("last_update", 0) == 0
        }

        if nodes_to_remove:
            G.remove_nodes_from(nodes_to_remove)
            removed = True  # Continua finché ci sono nodi da eliminare

    # **Fase 2: Mantenere solo la componente connessa più grande**
    if len(G.nodes) > 0:
        largest_component = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_component).copy()

    # **Fase 3: Ricostruire i dati filtrati con tutti i campi originali**
    filtered_nodes_data = []
    for n in G.nodes:
        node = node_map[n].copy()  # Copia i dati originali del nodo
        node["last_update_iso"] = convert_last_update_iso(
            node.get("last_update", 0)
        )  # Nuovo campo ISO
        filtered_nodes_data.append(node)

    filtered_channels = [
        edge
        for edge in edge_list
        if edge["node1_pub"] in G.nodes and edge["node2_pub"] in G.nodes
    ]

    return filtered_nodes_data, filtered_channels
