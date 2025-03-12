import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Lista dei grafi
graph_list = [
    "graphml_weighted/2025/snapshot_2025.graphml.graphml", 
    "graphml_weighted/2025/Subnetwork_Degree_Between_2_and_100000_snapshot_2025.graphml.graphml",
    "graphml_weighted/2025/Subnetwork_Degree_Between_2_and_612.0_snapshot_2025.graphml.graphml",
    "graphml_weighted/2025/Subnetwork_Degree_Between_2_and_101.0_snapshot_2025.graphml.graphml",
]

# Itera su ogni file di grafo
for graph_path in graph_list:
    G = nx.read_graphml(graph_path)

    # Se il grafo è diretto, lo converte in non diretto
    if G.is_directed():
        G = G.to_undirected(reciprocal=False)

    # Estrai le capacità dei canali (assumendo che siano nell'attributo 'capacity' degli archi)
    capacities = []
    for u, v, data in G.edges(data=True):
        if 'capacity' in data:
            try:
                cap_value = float(data['capacity'])
                capacities.append(cap_value)
            except ValueError:
                pass  # ignora valori non numerici

    # Verifica se sono state trovate capacità
    if not capacities:
        raise ValueError(f"Non sono state trovate capacità nei canali del grafo: {graph_path}")

    # Convertilo in un array numpy per una manipolazione più semplice
    capacities = np.array(capacities)
    total_capacity = capacities.sum()

    # Segmentazione in quartili (dividendo in 4 gruppi uguali in numero)
    capacities_sorted = np.sort(capacities)
    n = len(capacities_sorted)

    quartile_edges = [
        capacities_sorted[:int(0.25*n)],
        capacities_sorted[int(0.25*n):int(0.5*n)],
        capacities_sorted[int(0.5*n):int(0.75*n)],
        capacities_sorted[int(0.75*n):]
    ]

    # Calcola la capacità totale per ciascun quartile
    quartile_capacity_sums = [seg.sum() for seg in quartile_edges]
    quartile_percentage = [100 * s / total_capacity for s in quartile_capacity_sums]

    # Stampa dei risultati
    print(f"Segmentazione del grafo {graph_path} per quartili (basata sul numero di canali):")
    print(f"Primo 25% dei canali: {quartile_percentage[0]:.2f}% della capacità totale")
    print(f"Secondo 25% dei canali: {quartile_percentage[1]:.2f}% della capacità totale")
    print(f"Terzo 25% dei canali: {quartile_percentage[2]:.2f}% della capacità totale")
    print(f"Ultimo 25% dei canali: {quartile_percentage[3]:.2f}% della capacità totale")

    # Visualizzazione dei risultati con un grafico a barre
    # labels = ['0-25%', '25-50%', '50-75%', '75-100%']
    # plt.figure(figsize=(8, 5))
    # plt.bar(labels, quartile_percentage, color='skyblue', edgecolor='black')
    # plt.xlabel("Segmento dei canali (quantile)")
    # plt.ylabel("Percentuale della capacità totale (%)")
    # plt.title(f"Segmentazione della capacità dei canali per quartili ({graph_path})")
    # plt.ylim(0, max(quartile_percentage) * 1.2)
    # plt.grid(axis='y')
    # plt.show()
