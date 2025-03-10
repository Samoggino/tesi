import re
from pathlib import Path
import py4cytoscape as py4

# Funzione per ottenere l'anno dal nome del network
def get_year_from_network(network_name):
    match = re.search(r"(2019|2020|2021|2022|2023|2024|2025)", network_name)
    return match.group(0) if match else None

# Funzione per esportare un network in base all'anno
def export_network_by_year(network_name):
    year = get_year_from_network(network_name)

    if not year:
        print(f"Network senza anno, ignorato: {network_name}")
        return

    # Seleziona il network prima di esportarlo
    py4.set_current_network(network_name)

    output_folder = Path(f"/home/samoggino/VSC/tesi/graphml/cytoscape_exported/{year}")
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / f"{network_name}.graphml"

    py4.export_network(filename=str(output_file.resolve()), type='graphml')
    print(f"Esportato: {output_file}")

# Funzione per esportare tutti i network attivi in Cytoscape
def export_all_networks():
    network_list = py4.get_network_list()
    print("Network attivi:", network_list)

    for network_name in network_list:
        export_network_by_year(network_name)

# Connettiti a Cytoscape
py4.cytoscape_ping()

# Esegui l'esportazione dei network
export_all_networks()
