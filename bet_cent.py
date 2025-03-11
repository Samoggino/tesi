import networkx as nx
import plotly.graph_objects as go
import numpy as np

# Carica il grafo del 2025
G = nx.read_graphml(f"graphml_weighted/2025/snapshot_2025.graphml.graphml")

# Converte il grafo diretto in un grafo non diretto
G_undirected = G.to_undirected()

# Trova tutte le componenti connesse
connected_components = list(nx.connected_components(G_undirected))

# Trova la componente connessa più grande
largest_component = max(connected_components, key=len)

# Crea un nuovo grafo che contiene solo i nodi della componente più grande
G_largest = G.subgraph(largest_component)

# Estrai gli attributi BetweennessCentrality e Degree dal grafo rimanente
degree_values = [data['Degree'] for _, data in G_largest.nodes(data=True)]
betweenness_values = [data['BetweennessCentrality'] for _, data in G_largest.nodes(data=True)]

# Estrai le etichette (alias) dei nodi
node_aliases = [data.get('alias', 'No Alias') for _, data in G_largest.nodes(data=True)]

# Crea una lista di etichette che mostreranno sempre per i nodi con degree > 500
always_labels = ['' if degree <= 950 else alias for degree, alias in zip(degree_values, node_aliases)]

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
    title='Relazione tra Degree e Betweenness Centrality (Componente Connessa Più Grande)',
    xaxis_title='Degree',
    yaxis_title='Betweenness Centrality',
    showlegend=False  # Disabilita la legenda
)

# Esporta il grafico come PNG
fig.write_image("graph_output.png")

print("Il grafico è stato salvato come 'graph_output.png'.")
