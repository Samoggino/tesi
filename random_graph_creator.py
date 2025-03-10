import networkx as nx

# 1. Leggere il grafo esistente
graph_file = "graphml/snapshot_2025.graphml"
G_existing = nx.read_graphml(graph_file)

# 2. Estrazione del numero di nodi e archi dal grafo esistente
num_nodes = len(G_existing.nodes())
num_edges = len(G_existing.edges())

# 3. Calcolare la probabilità p per il modello Erdős–Rényi
p = num_edges / (num_nodes * (num_nodes - 1) / 2)

# 4. Creare il grafo randomico con la stessa dimensione
G_random = nx.erdos_renyi_graph(num_nodes, p)

# 5. Esportare il grafo randomico in un file GraphML
random_graph_file = "random_graph.graphml"
nx.write_graphml(G_random, random_graph_file)

# 6. Stampare alcune informazioni sul grafo generato
print(f"Numero di nodi: {G_random.number_of_nodes()}")
print(f"Numero di archi: {G_random.number_of_edges()}")
print(f"Probabilità p: {p}")
print(f"Grafo randomico salvato in: {random_graph_file}")