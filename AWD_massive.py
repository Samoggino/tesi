import os
import networkx as nx

def average_weighted_degree(G, weight="weight"):
    # Calcola la somma dei pesi di tutti gli archi
    total_weight = sum(data.get(weight, 1) for _, _, data in G.edges(data=True))
    num_nodes = G.number_of_nodes()
    # Formula dell'AWD: (2 * somma_pesi) / numero_nodi
    return (2 * total_weight) / num_nodes if num_nodes > 0 else 0

# Cartella contenente i grafi pesati con la struttura {anno}/...
weighted_root = "graphml_weighted"

# Itera ricorsivamente su tutte le directory e file nella cartella pesata
for dirpath, dirnames, filenames in os.walk(weighted_root):
    for filename in filenames:
        if filename.endswith(".graphml"):
            file_path = os.path.join(dirpath, filename)
            print(f"Elaborazione di: {file_path}")
            G = nx.read_graphml(file_path)
            avg_awd = average_weighted_degree(G)
            print(f"AWD per {file_path}: {avg_awd}")
