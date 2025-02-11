import json

# Carica il JSON
with open("json/lnd_1_graph_2025-02-06_00-00-21-filtered.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Rimuove il campo "features" da tutti i nodi
for node in data.get("nodes", []):
    node.pop("features", None)
    node.pop("addresses", None)
    node.pop("custom_records", None)
    
for edge in data.get("edges", []):
    edge.pop("custom_records", None)
    edge.pop("node1_policy", None)
    edge.pop("node2_policy", None)
    edge.pop("chan_point", None)

print("Ci sono {} nodi e {} archi.".format(len(data.get("nodes", [])), len(data.get("edges", []))))

# Salva il JSON modificato
with open("json/filtered_2025-02-06.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
