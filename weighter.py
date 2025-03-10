import networkx as nx
from decimal import Decimal

# Carica il grafo dal file GraphML

nomi_grafo = [
    "snapshot_2019",
    "snapshot_2020",
    "snapshot_2021",
    "snapshot_2022",
    "snapshot_2023",
    "snapshot_2024",
    "snapshot_2025-02-06-unfiltered",
]

for nome_grafo in nomi_grafo:

    print("Sto lavorando su", nome_grafo)

    G = nx.read_graphml("graphml/" + nome_grafo + ".graphml")

    # Dividi per 1.000.000 per ottenere i valori in satoshi
    normalization_factor = 1_000_000

    # Aggiungi il peso normalizzato agli archi
    for u, v, data in G.edges(data=True):
        capacity = float(Decimal(data.get("capacity", 1)) / normalization_factor)
        data["weight"] = 1 / capacity if capacity > 0 else 1  # Evita divisioni per zero

    # Salva il grafo aggiornato in un nuovo file
    nx.write_graphml(G, "graphml/weighted/" + nome_grafo + "_with_weights.graphml")
