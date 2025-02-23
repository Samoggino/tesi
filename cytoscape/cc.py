import networkx as nx

folder = "../graphml/"

file = "snapshot_2025.graphml" # tutti i nodi
# file = "Subnetwork_Degree_Between_2_and_100000_snapshot_2025.graphml" # nodi con più di 2 canali
# file = "Subnetwork_Degree_Between_2_and_612.0_snapshot_2025.graphml" # top 10 excluded
# file = "Subnetwork_Degree_Between_2_and_101.0_snapshot_2025.graphml" # top 100 excluded
file = "Subnetwork_Degree_Between_1_and_101.0_snapshot_2025.graphml" # top 100 excluded, min 1

# Carica il grafo
graph = nx.read_graphml(folder + file)
graph_total = nx.read_graphml(folder + "snapshot_2025.graphml")

# Trova tutte le componenti connesse
if nx.is_directed(graph):
    components = list(nx.weakly_connected_components(graph))  # oppure strongly
else:
    components = list(nx.connected_components(graph))


# Calcola la dimensione di ciascuna componente
component_sizes = [len(component) for component in components]

# Stampa il numero di componenti connesse
print(f"\nIl grafo ha {len(components)} componenti connesse.")

# inserisci le componenti in una mappa q.tà nodi -> numero componenti
component_size_map = {}
for size in component_sizes:
    if size in component_size_map:
        component_size_map[size] += 1
    else:
        component_size_map[size] = 1

# ordina la mappa per q.tà nodi dal più grande al più piccolo
sorted_map = dict(
    sorted(component_size_map.items(), key=lambda item: int(item[0]), reverse=True)
)

# Stampa la mappa in modo carino
print("\nMappa dimensioni componenti:")
for size, count in sorted_map.items():
    print(f"Totale nodi:\t{size}\t {count}\t componenti connesse")

# Dimensione della componente più grande
largest_component_size = max(component_sizes)
print(f"\nLa componente più grande ha {largest_component_size} nodi.")

# Numero totale di nodi iniziali
total_nodes = graph_total.number_of_nodes() - 1 # -1 per il nodo vuoto da cui parte l'analisi

# Trova la componente più grande nel grafo filtrato
largest_component = max(components, key=len)
largest_component_set = len(set(largest_component))

# Trova i nodi che esistono nel grafo originale, ma non sono nella componente principale

# Stampa i risultati
print(f"\nNumero totale di nodi iniziali: {total_nodes}")
print(f"Numero di nodi nella componente principale: {largest_component_set}")
print(f"Numero di nodi non connessi alla componente principale: {total_nodes - largest_component_set}")
