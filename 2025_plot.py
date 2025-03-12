import pandas as pd
import matplotlib.pyplot as plt

# Percorso del file CSV (modifica se necessario)
csv_file = "data.csv"

# Legge il CSV
df = pd.read_csv(csv_file)

# Converte la colonna 'Snapshot' in intero (rappresenta l'anno)
df["Snapshot"] = df["Snapshot"].astype(int)

# Converte le colonne in float gestendo il separatore decimale
df["Clustering"] = df["Clustering"].apply(lambda x: float(str(x).replace(",", ".")))
df["APL"] = df["APL"].apply(lambda x: float(str(x).replace(",", ".")))
df["Avg Neighbors"] = df["Avg Neighbors"].apply(
    lambda x: float(str(x).replace(",", "."))
)
df["Centralization"] = df["Centralization"].apply(
    lambda x: float(str(x).replace(",", "."))
)
df["σ"] = df["σ"].apply(lambda x: float(str(x).replace(",", ".")))
df["CC"] = df["CC"].apply(lambda x: float(str(x).replace(",", ".")))

# Filtra i dati per il 2025
df_2025 = df[df["Snapshot"] == 2025]

# Imposta l'ordine delle categorie
category_order = [
    "unfiltered",
    "min_2",
    "top10 excluded & min_2",
    "top100 excluded & min_2",
]

# Ordina il DataFrame in base all'ordine delle categorie
df_2025["Categoria"] = pd.Categorical(
    df_2025["Categoria"], categories=category_order, ordered=True
)
df_2025 = df_2025.sort_values("Categoria")


# Funzione per creare i grafici
def plot_metric(metric, ylabel, title, color):
    plt.figure(figsize=(8, 5))
    plt.plot(
        ["unfiltered", "almeno due canali", "top10", "top100"], df_2025[metric], marker="o", linestyle="-", color=color
    )
    plt.xlabel("")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Crea i grafici per ogni metrica
# plot_metric("Clustering", "CC", "Clustering Coefficient (CC)", "blue")
# plot_metric("APL", "APL", "Average Path Length (APL)", "red")
# plot_metric("Avg Neighbors", "AND", "Average Neighbors Degree (AND)", "green")
# plot_metric("Centralization", "NC", "Network Centralization (NC)", "purple")
# plot_metric("σ", "σ", "Sigma σ", "orange")
plot_metric("CC", "CC", "Connected Components", "firebrick")