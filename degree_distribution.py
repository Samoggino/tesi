import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

graph_files = {
    "All Nodes": "graphml_weighted/2025/snapshot_2025.graphml",
    "TOP 10 Excluded": "graphml_weighted/2025/Subnetwork_Degree_Between_2_and_619_snapshot_2025.graphml.graphml",
    "TOP 100 Excluded": "graphml_weighted/2025/Subnetwork_Degree_Between_2_and_105_snapshot_2025.graphml.graphml",
}

def plot_degree_distribution_loglog(graph_path, title_suffix, num_bins=200):
    G = nx.read_graphml(graph_path)

    node_degrees = [degree for node, degree in G.degree()]

    # I gradi devono essere validi (>= 1 per logaritmo) anche se probabilmente già lo sono
    node_degrees = [d for d in node_degrees if d >= 1]

    min_log_k = np.log10(max(1, min(node_degrees)))
    max_log_k = np.log10(max(node_degrees))

    bins = np.logspace(min_log_k, max_log_k, num_bins)

    plt.figure(figsize=(10, 7)) 
    plt.hist(node_degrees, bins=bins, density=True, edgecolor='black', alpha=0.7)

    plt.xscale('log')
    plt.yscale('log')

    plt.xlabel("Degree k (log scale)")
    plt.ylabel("Frequency P(k) (log scale)")
    plt.title(f"Degree Distribution (Log-Log) - {title_suffix}")

    plt.tight_layout() 
    plt.savefig(f"plot/dd/dd_log-log_{title_suffix}.png", dpi=300) # Salva il plot in PNG
    # plt.show()

# Loop per ogni grafo
for title, path in graph_files.items():
    print(f"Generando plot per: {title}")
    plot_degree_distribution_loglog(path, title)