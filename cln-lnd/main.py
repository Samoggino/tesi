from read_write import read_input_json, write_output_json
from channel_processing import process_channels
from node_conversion import convert_nodes

anno = "2021"

# Specifica dei nomi dei file
input_file = '../topology/lntopo/' + str(anno) + '.json'
output_file = '../json/lnd_' + str(anno) + '.json'

# Lettura dei dati di input
data = read_input_json(input_file)
cln_nodes = data['nodes']
cln_channels = data['adjacency']

# Elaborazione dei canali
print("Inizio elaborazione dei canali...")
channel_dict = process_channels(cln_channels)
print("Fine elaborazione dei canali.")

# Conversione dei nodi
print("Inizio conversione dei nodi...")
lnd_nodes = convert_nodes(cln_nodes)
print(f"Numero di nodi: {len(lnd_nodes)}")

# Debug: Stampa i canali elaborati
print(f"Canali elaborati: {len(channel_dict)}")

# Conversione dei canali in formato LND
lnd_channels = []
for scid, info in channel_dict.items():
    if info["node1_pub"] is not None and info["node2_pub"] is not None:
        lnd_channels.append({
            "channel_id": scid,
            "last_update": info["last_update"],
            "node1_pub": info["node1_pub"],
            "node2_pub": info["node2_pub"],
            "capacity": str(info["max_capacity_msat"] // 1000)  # Convertiamo msat in satoshi
        })
    else:
        print(f"Canale {scid} ignorato: nodi invalidi")

print(f"Numero di canali validi: {len(lnd_channels)}")

# Costruzione del JSON finale
final_json = {
    "nodes": lnd_nodes,
    "edges": lnd_channels
}

# Scrittura del file di output
write_output_json(output_file, final_json)
print(f"File di output scritto in: {output_file}")
