import os
import networkx as nx
from decimal import Decimal

# Cartella di origine e destinazione
input_root = "graphml/cytoscape_exported"  # cartella con la struttura {anno}
output_root = "graphml_weighted"  # nuova cartella in cui salvare i file pesati

# Itera ricorsivamente sui file all'interno di input_root
for dirpath, dirnames, filenames in os.walk(input_root):
    for filename in filenames:
        if filename.endswith(".graphml"):
            input_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(input_path, input_root)
            output_path = os.path.join(output_root, relative_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            print("Elaborando:", input_path)
            G = nx.read_graphml(input_path)

            normalization_factor = 1_000_000
            # Aggiungi il peso normalizzato agli archi
            for idx, (u, v, data) in enumerate(G.edges(data=True)):
                # Prendi il valore di capacity o default a "1"
                cap_val = data.get("capacity", 1)
                try:
                    capacity = float(Decimal(cap_val) / normalization_factor)
                except Exception as e:
                    print(f"Errore nella conversione di capacity '{cap_val}' per l'arco {u}-{v}: {e}")
                    capacity = 1 / normalization_factor  # fallback
                data["weight"] = 1 / capacity if capacity > 0 else 1

                # Stampa il valore per i primi 3 archi per debug
                if idx < 3:
                    print(f"Arco {u}-{v}: capacity = {cap_val}, normalizzata = {capacity}, weight = {data['weight']}")

            nx.write_graphml(G, output_path)
            print("Salvato in:", output_path)
            print("-" * 40)
