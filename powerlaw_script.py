import networkx as nx
import matplotlib.pyplot as plt
import powerlaw

# Anni da analizzare
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
alpha_values = []
xmin_values = []

# Analisi per ogni anno
for year in years:
    G = nx.read_graphml(f"graphml_weighted/{year}/snapshot_{year}.graphml.graphml")
    node_degrees = [degree for node, degree in G.degree()]
    
    power_law_fit = powerlaw.Fit(node_degrees)
    alpha_values.append(power_law_fit.alpha)
    xmin_values.append(power_law_fit.xmin)
    
    print(f"Anno {year}: α = {power_law_fit.alpha}, xmin = {power_law_fit.xmin}")

# Creazione del grafico
fig, ax1 = plt.subplots(figsize=(8, 6))

# Prima curva (Esponente α)
color = 'tab:blue'
ax1.set_xlabel("Anno")
ax1.set_ylabel("Esponente α", color=color)
ax1.plot(years, alpha_values, marker='o', color=color, label="Esponente α")
ax1.tick_params(axis='y', labelcolor=color)

# Secondo asse Y per xmin
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel("xmin", color=color)
ax2.plot(years, xmin_values, marker='s', linestyle="dashed", color=color, label="xmin")
ax2.tick_params(axis='y', labelcolor=color)

# Titolo e griglia
plt.title("Evoluzione di α e xmin nella Lightning Network (2019-2025)")
ax1.grid(True, linestyle="--", alpha=0.6)

# Mostra il grafico
plt.show()