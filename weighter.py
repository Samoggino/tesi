import networkx as nx
from decimal import Decimal

# Carica il grafo dal file GraphML
G = nx.read_graphml("graphml/snapshot_2019.graphml")

# Supponiamo che "capacity" sia espresso in millasatoshi
normalization_factor = 1000000  # Dividi per 1.000.000 per ottenere i valori in satoshi

# Aggiungi il peso normalizzato agli archi
for u, v, data in G.edges(data=True):
    # Converte in float
    data["weight"] = float(Decimal(data.get("capacity", 1)) / normalization_factor)

# Salva il grafo aggiornato in un nuovo file
nx.write_graphml(G, "graphml/snapshot_2019_with_weights.graphml")
