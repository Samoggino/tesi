import networkx as nx

path = "graphml_weighted/2025/snapshot_2025.graphml"
G = nx.read_graphml(path)

# non so se serva convertirlo in non diretto, ma se lo è, lo faccio
if G.is_directed():
    G = G.to_undirected()

degree_centrality = nx.degree_centrality(G)

def network_centralization(centrality_dict):
    n = len(centrality_dict)
    if n <= 2:
        return 0.0  # Non ha senso definire la centralizzazione con meno di 3 nodi

    max_centrality = max(centrality_dict.values())
    sum_diffs = sum(max_centrality - c for c in centrality_dict.values())

    # Normalizzazione
    max_sum = (n - 1) * (1 - (1 / (n - 1)))
    return sum_diffs / max_sum

centralization_value = network_centralization(degree_centrality)

# === Output ===
print(f"Network centralization (degree-based): {centralization_value:.3f}")

import networkx as nx

# problema stupido con GraphML che ha attributi duplicati "weight" sia nei nodi che negli archi
def clean_graphml_weights(path, output_file):
    
    G = nx.read_graphml(path)

    # Rimuovi attributi duplicati "weight" da nodi
    for node in G.nodes():
        if isinstance(G.nodes[node], dict):
            keys = list(G.nodes[node].keys())
            for k in keys:
                if k.lower() == 'weight':
                    # Rimuovi o rinomina se vuoi tenere
                    del G.nodes[node][k]

    # Rimuovi attributi duplicati "weight" da archi
    for u, v, data in G.edges(data=True):
        if isinstance(data, dict):
            keys = list(data.keys())
            for k in keys:
                if k.lower() == 'weight':
                    del data[k]

    nx.write_graphml(G, output_file)

# Percorsi file
cleaned_file = "cleaned_graphml_no_weight.graphml"

# Pulisci
clean_graphml_weights(path, cleaned_file)

import igraph as ig

g = ig.Graph.Read_GraphML(cleaned_file)

# nodi e archi per check al volo
print(f"Numero di nodi: {g.vcount()}")
print(f"Numero di archi: {g.ecount()}")

centrality = g.degree(mode="all")
n = len(centrality)
max_c = max(centrality)
sum_diff = sum(max_c - c for c in centrality)
max_sum = (n - 1) * (n - 2)
centralization = sum_diff / max_sum if max_sum != 0 else 0.0

print(f"Degree centralization (normalizzata): {centralization:.3f}")
