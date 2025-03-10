import networkx as nx


def average_weighted_degree(G, weight="weight"):
    total_weight = sum(
        data.get(weight, 1) for _, _, data in G.edges(data=True)
    )  # Somma tutti i pesi degli archi
    num_nodes = G.number_of_nodes()
    return (2 * total_weight) / num_nodes if num_nodes > 0 else 0  # Formula AWD


nomi_grafo = [
    "snapshot_2019",
    "snapshot_2020",
    "snapshot_2021",
    "snapshot_2022",
    "snapshot_2023",
    "snapshot_2024",
    "snapshot_2025",
]

for nome_grafo in nomi_grafo:
    G = nx.read_graphml("graphml/weighted/" + nome_grafo + "_with_weights.graphml")
    # Calcola l'AWD globale
    average_awd = average_weighted_degree(G)

    print(f"AWD per {nome_grafo}: {average_awd}")
