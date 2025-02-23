import networkx as nx

# Carica il grafo da un file GraphML
G = nx.read_graphml("graphml/snapshot_2019.graphml")

# Filtra i nodi con grado < 2
G_copy = G.copy()  # Crea una copia per non modificare il grafo originale
nodes_to_remove = [node for node, degree in G.degree() if degree < 2]
G_copy.remove_nodes_from(nodes_to_remove)

# Ottieni i 100 nodi con il grado più alto (li escluderai)
top_100_nodes = sorted(G_copy.degree(), key=lambda x: x[1], reverse=True)[:100]
top_100_node_ids = [node for node, degree in top_100_nodes]

# Escludi i 100 nodi con il grado più alto
G_copy_excluded = G_copy.copy()
G_copy_excluded.remove_nodes_from(top_100_node_ids)

# Calcola il grado massimo del sottografo rimanente
max_degree = max(dict(G_copy_excluded.degree()).values())

# print max degree
print(f"Max degree: {max_degree}")

# Calcola la degree centralization
degree_centralization = sum(
    max_degree - degree for node, degree in G_copy_excluded.degree()
) / ((len(G_copy_excluded) - 1) * (len(G_copy_excluded) - 2))

print(f"Nodes remaining after excluding top 100 nodes: {len(G_copy_excluded)}")


print(f"Degree Centralization after excluding top 100 nodes: {degree_centralization}")
