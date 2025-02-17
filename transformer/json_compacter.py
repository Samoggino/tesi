import json

# Carica il JSON
with open("json/lnd_2023-filtered.json", "r", encoding="utf-8") as f:
    data = json.load(f)

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
with open("json/compacted_2023.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
