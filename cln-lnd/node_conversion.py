from datetime import datetime

# Funzione per convertire i nodi in formato LND
def convert_nodes(cln_nodes):
    lnd_nodes = []
    for node in cln_nodes:
        if 'addresses' in node and node["addresses"]:
            addresses = []
            for addr in node["addresses"].split(","):
                if "://" in addr:
                    _, addr_val = addr.split("://", 1)
                    addresses.append({"network": "tcp", "addr": addr_val})
                else:
                    addresses.append({"network": "tcp", "addr": addr})
        else:
            addresses = []

        timestamp = node.get("timestamp", 0)  # Usa 0 se il campo 'timestamp' non esiste
        
        lnd_nodes.append({
            "last_update": timestamp,
            "pub_key": node["id"],
            "alias": node["alias"] if "alias" in node else node["id"],
            "color": "#" + node["rgb_color"] if "rgb_color" in node else "#FFFFFF",
            "addresses": addresses,
            "last_update_iso": datetime.utcfromtimestamp(timestamp).isoformat()
        })
    
    return lnd_nodes
