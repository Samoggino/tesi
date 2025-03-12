import networkx as nx
import matplotlib.pyplot as plt

# 1. Carica il grafo da GraphML
G = nx.read_graphml(
    "graphml_weighted/2025/Subnetwork_Degree_Between_2_and_100000_snapshot_2025.graphml.graphml"
)

# 2. Estrai i gradi dei nodi (grado k)
node_degrees = [degree for node, degree in G.degree()]

# 3. Traccia un grafico log-log della distribuzione dei gradi
plt.figure(figsize=(8, 6))
plt.hist(node_degrees, bins=50, density=True, log=True)
plt.xlabel("Log(Degree k)")
plt.ylabel("Log(Frequency P(k))")
plt.title("Degree Distribution (Log-Log)")

# mostra il grafico
plt.show()
