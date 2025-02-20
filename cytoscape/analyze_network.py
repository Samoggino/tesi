import py4cytoscape as py4  # type: ignore
import pandas as pd  # type: ignore
import csv
import os

# Funzione per generare un nome di file univoco
def get_unique_filename(base_name, extension):
    counter = 1
    while os.path.exists(f"{base_name}_{counter}{extension}"):
        counter += 1
    return f"{base_name}_{counter}{extension}"

# Ottieni l'elenco di tutte le reti nel progetto
network_list = ['snapshot_2019.graphml', 'snapshot_2020.graphml', 'snapshot_2021.graphml', 'snapshot_2022.graphml', 'snapshot_2023.graphml', 'snapshot_2024.graphml', 'snapshot_2025.graphml']
# network_list = ['snapshot_2019.graphml']

# Crea una lista per raccogliere i risultati
analysis_results = []

# Itera su ogni rete
for network_name in network_list:
    # Imposta la rete corrente
    py4.set_current_network(network_name)
    
    print(f"Grafo selezionato: {network_name}")
    
    # Ottieni la tabella dei nodi
    node_table = py4.get_table_columns('node')
    
    # Converte la tabella in un DataFrame pandas
    df = pd.DataFrame(node_table)
    
    # Assicurati che la colonna 'Degree' sia numerica
    df['Degree'] = pd.to_numeric(df['Degree'], errors='coerce')
    
    # Rimuove eventuali valori NaN nella colonna 'Degree'
    df = df.dropna(subset=['Degree'])
    
    # Crea una lista di tuple (node_suid, degree)
    nodes_with_degrees = [(pub_key, degree) for pub_key, degree in zip(df['pub_key'], df['Degree'])]
    
    # Ordina i nodi per grado in ordine decrescente
    nodes_with_degrees.sort(key=lambda x: x[1], reverse=True)
    
    # Grado del decimo nodo
    limit = 100
    degree_of_tenth_node = nodes_with_degrees[limit-1][1] if len(nodes_with_degrees) > limit else nodes_with_degrees[-1][1]
    # degree_of_tenth_node = 100000
    min_degree = 2
    # min_degree = 0
    
    # Crea un filtro per selezionare nodi con grado maggiore di 2 e minore o uguale al grado del decimo nodo
    filter_name = f"DegreeBetween2And{degree_of_tenth_node}"
    criterion = [min_degree, degree_of_tenth_node]  # Seleziona nodi con grado tra 2 e il grado del decimo nodo
    py4.filters.create_degree_filter(filter_name, criterion, predicate='BETWEEN', edge_type='ANY', hide=False, apply=True)
    
    # Ottieni la lista dei nodi selezionati
    selected_nodes = py4.get_selected_nodes(node_suids=True, network=network_name)

    if not selected_nodes:
        print(f"Nessun nodo soddisfa il criterio di selezione nella rete {network_name}.")
    else:
        # Crea una nuova sottorete con i nodi selezionati
        subnetwork_suid = py4.create_subnetwork(nodes=selected_nodes,subnetwork_name=f'Subnetwork_Degree_Between_{min_degree}_and_{degree_of_tenth_node}_{network_name}',network=network_name)
        
        # Imposta la sottorete come rete corrente
        py4.set_current_network(subnetwork_suid)
        
        print(f"Analizzo la rete {network_name}")
        
        # Ottieni la tabella dei nodi della sottorete
        subnetwork_node_table = py4.get_table_columns('node')
        subnetwork_df = pd.DataFrame(subnetwork_node_table)
        
        # Assicurati che la colonna 'Degree' sia numerica e calcola la mediana
        subnetwork_df['Degree'] = pd.to_numeric(subnetwork_df['Degree'], errors='coerce')
        median_degree = subnetwork_df['Degree'].median()
        average_degree = subnetwork_df['Degree'].mean()
        
        # Esegui l'analisi della rete sulla sottorete
        results = py4.tools.analyze_network(directed=False)
        
        # Aggiungi la mediana del degree ai risultati
        results['Median_Degree'] = median_degree
        results['Average_Degree'] = average_degree
        
        # rimuovi la colonna time dal result
        results.pop('time', None)
        
        # Aggiungi i risultati all'elenco
        analysis_results.append({'network': network_name, **results})
        
        # Elimina la sottorete
        py4.delete_network(subnetwork_suid)

        print(f"Rete {network_name} analizzata.")

# Genera un nome di file univoco per il CSV
csv_filename = get_unique_filename('network_analysis_results', '.csv')

# Esporta i risultati in un file CSV
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=analysis_results[0].keys(), delimiter='\t')
    writer.writeheader()
    for result in analysis_results:
        for key in result:
            if isinstance(result[key], float):
                result[key] = str(result[key]).replace('.', ',')  # Sostituisce . con ,
        writer.writerow(result)

print(f"Risultati esportati in {csv_filename}.")
