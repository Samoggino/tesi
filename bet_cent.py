import networkx as nx
import plotly.graph_objects as go
import numpy as np

from cytoscape.utils import get_unique_filename

# Carica il grafo del 2025

n_nodi = 16688
n_canali = 50565

G = nx.read_graphml(f"graphml_weighted/2025/snapshot_2025.graphml.graphml")
# G = nx.read_graphml(f"graphml_weighted/2025/Subnetwork_Degree_Between_2_and_100000_snapshot_2025.graphml.graphml")
# G = nx.read_graphml(f"graphml_weighted/2025/Subnetwork_Degree_Between_2_and_612.0_snapshot_2025.graphml.graphml")

# Converte il grafo diretto in un grafo non diretto
G_undirected = G.to_undirected()

# Trova tutte le componenti connesse
connected_components = list(nx.connected_components(G_undirected))

# Trova la componente connessa più grande
largest_component = max(connected_components, key=len)

# Crea un nuovo grafo che contiene solo i nodi della componente più grande
G_largest = G.subgraph(largest_component)

# salva il grafo in formato GraphML
nx.write_graphml(G_largest, "graphml_weighted/2025/largest_component_2025.graphml")

# Estrai gli attributi BetweennessCentrality, Degree e Alias dai nodi
degree_values = []
betweenness_values = []
always_labels = []

for _, data in G_largest.nodes(data=True):
    degree = data['Degree']
    betweenness = data['BetweennessCentrality']
    alias = data.get('alias', 'No Alias')

    degree_values.append(degree)
    betweenness_values.append(betweenness)

    # Assegna l'etichetta solo ai nodi con degree > 950
    always_labels.append('' if degree <= 950 else alias)


# Calcola la correlazione tra Degree e Betweenness Centrality
correlation = np.corrcoef(degree_values, betweenness_values)[0, 1]

# Crea il grafico con Plotly
fig = go.Figure()

# Aggiungi i punti al grafico (scatter plot)
fig.add_trace(go.Scatter(
    x=degree_values, 
    y=betweenness_values, 
    mode='markers+text',
    marker=dict(size=12, color='blue', opacity=0.7),
    text=always_labels,  # Mostra etichetta sempre per i nodi con degree > 500
    textposition="top center",  # Posiziona il testo sopra i punti
))

# Aggiungi titolo e etichette agli assi
fig.update_layout(
    title=f'Degree by Betweenness Centrality',
    xaxis_title='Degree',
    yaxis_title='Betweenness Centrality',
    showlegend=False  # Disabilita la legenda
)

# Aggiungi annotazioni per il numero di nodi e il numero di archi
num_nodes = G_largest.number_of_nodes()
num_edges = G_largest.number_of_edges()

# Calcola la percentuale di nodi e canali nella componente connessa più grande
percentuale_nodi = (num_nodes / n_nodi) * 100
percentuale_canali = (num_edges / n_canali) * 100

# Aggiungi annotazione con nodi, canali e correlazione
fig.add_annotation(
    x=0.5, y=1.10, 
    text=f'Nodi: {num_nodes} ({percentuale_nodi:.2f}% del totale) , Canali: {num_edges} ({percentuale_canali:.2f}% del totale) ---- Correlazione: {correlation:.3f}',
    showarrow=False,
    font=dict(size=12),
    xref="paper", yref="paper",
    align="center"
)


# Salva il grafico come immagine
filename = get_unique_filename("graph_output",".png")
fig.write_image(filename)

print(f"Correlazione tra Degree e Betweenness Centrality: {correlation}")
print("Il grafico è stato salvato come immagine:", filename)
