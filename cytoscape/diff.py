# diff.py - Esempio di confronto tra due reti in Cytoscape
import py4cytoscape as py4

# Controlla la connessione a Cytoscape
py4.cyrest.cy_ping()
# Ottieni la lista delle reti disponibili in Cytoscape
networks = py4.cyrest.network.get_all()
print("Reti disponibili:", networks)
# Seleziona le reti da confrontare
network1 = networks[0]  # Prima rete
network2 = networks[2]  # Seconda rete
# Ottieni i nodi della prima rete
nodes_network1 = py4.cyrest.network.get_nodes(network1)
nodes_network1_set = set(nodes_network1)

# Ottieni i nodi della seconda rete
nodes_network2 = py4.cyrest.network.get_nodes(network2)
nodes_network2_set = set(nodes_network2)
# Nodi presenti nella prima rete ma non nella seconda
nodes_in_network1_not_in_network2 = nodes_network1_set - nodes_network2_set
print(
    "Nodi presenti nella prima rete ma non nella seconda:",
    nodes_in_network1_not_in_network2,
)

# Nodi presenti nella seconda rete ma non nella prima
nodes_in_network2_not_in_network1 = nodes_network2_set - nodes_network1_set
print(
    "Nodi presenti nella seconda rete ma non nella prima:",
    nodes_in_network2_not_in_network1,
)
