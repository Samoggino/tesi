import networkx as nx
import matplotlib.pyplot as plt
import powerlaw  # Una libreria per l'adattamento della legge di potenza

# 1. Carica il grafo da GraphML
G = nx.read_graphml("graphml_weighted/2025/snapshot_2025.graphml.graphml")

# 2. Estrai i gradi dei nodi (grado k)
node_degrees = [degree for node, degree in G.degree()]

# 3. Traccia un grafico log-log della distribuzione dei gradi
plt.figure(figsize=(8, 6))
plt.hist(node_degrees, bins=50, density=True, log=True)
plt.xlabel("Log(Degree k)")
plt.ylabel("Log(Frequency P(k))")
plt.title("Degree Distribution (Log-Log)")
plt.show()

# 4. Adatta i dati a una legge di potenza usando powerlaw
power_law_fit = powerlaw.Fit(node_degrees)
gamma = power_law_fit.alpha  # Esponente gamma della legge di potenza
k_min = power_law_fit.xmin  # Valore minimo di k (grado)

print(f"Esponente gamma (α): {gamma}")
print(f"Valore minimo di k (xmin): {k_min}")

# 5. Verifica la qualità dell'adattamento
R, p_value = power_law_fit.distribution_compare("power_law", "exponential")
print(f"R: {R}, p-value: {p_value}")

# Se R è positivo e il p-value è basso, il modello di legge di potenza è migliore
if p_value < 0.05:
    print("Il grafo segue una legge di potenza!")
else:
    print("Il grafo non segue una legge di potenza.")
