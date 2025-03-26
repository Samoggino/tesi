import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Percorso del file CSV (modifica se necessario)
csv_file = "data.csv"

# Legge il CSV
df = pd.read_csv(csv_file)

# Converte la colonna 'Snapshot' in intero (rappresenta l'anno)
df["Snapshot"] = df["Snapshot"].astype(int)

important_metrics = ["Clustering", "APL", "Avg Neighbors", "Centralization", "σ", "CC"]

# Converte le colonne in float gestendo il separatore decimale
for col in important_metrics:
    df[col] = df[col].apply(lambda x: float(str(x).replace(",", ".")))

# Ordine delle categorie per l'asse x
category_order = [
    "unfiltered",
    "min_2",
    "top10 excluded & min_2",
    "top100 excluded & min_2",
]

# Crea un array numerico per le categorie (0, 1, 2, 3)
x_positions = np.arange(len(category_order))

# Ottiene gli anni ordinati (dal 2019 al 2025)
sorted_years = sorted(df["Snapshot"].unique())
n_years = len(sorted_years)
# Fattore per l'offset orizzontale (puoi modificarlo per aumentare/diminuire la separazione)
offset_factor = 0.0

# Funzione per creare i grafici
def plot_metric(metric, ylabel, title, use_log=False):
    plt.figure(figsize=(8, 5))
    for i, year in enumerate(sorted_years):
        # Calcola un offset per ogni anno: distribuito in modo simmetrico
        offset = (i - (n_years - 1) / 2) * offset_factor
        # Filtra i dati per l'anno corrente e imposta l'ordine delle categorie
        df_year = df[df["Snapshot"] == year].copy()
        df_year["Categoria"] = pd.Categorical(df_year["Categoria"], categories=category_order, ordered=True)
        df_year = df_year.sort_values("Categoria")
        # Le posizioni x per questo anno saranno gli x originali + offset
        x_vals = x_positions + offset
        plt.plot(
            x_vals,
            df_year[metric].values,
            marker="o",
            linestyle="-",
            label=str(year)
        )
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(x_positions, ["unfiltered", "min_2", "top10", "top100"])
    if use_log:
        plt.yscale("log")
    plt.legend(title="Anno")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Crea i grafici per ogni metrica
# Aggiungi use_log=True se desideri usare la scala logaritmica per l'asse y
# plot_metric("Clustering", "CC", "Clustering Coefficient (CC)")
# plot_metric("APL", "APL", "Average Path Length (APL)")
# plot_metric("Avg Neighbors", "AND", "Average Neighbors Degree (AND)")
# plot_metric("Centralization", "NC", "Network Centralization (NC)")
# plot_metric("σ", "σ", "Sigma σ")
plot_metric("CC", "Connected Components", "Connected Components")


# def plot_metric_unfiltered(metric, ylabel, title, use_log=False):
#     plt.figure(figsize=(8, 5))
#     df_unfiltered = df[df["Categoria"] == "unfiltered"]
#     plt.plot(
#         sorted_years,
#         df_unfiltered.groupby("Snapshot")[metric].mean(),
#         marker="o",
#         linestyle="-",
#         label=metric
#     )
#     plt.xlabel("Anno")
#     plt.ylabel(ylabel)
#     plt.title(title)
#     if use_log:
#         plt.yscale("log")
#     plt.grid(True)
#     plt.xticks(sorted_years)
#     plt.show()

# # Creazione dei grafici per ogni metrica
# plot_metric_unfiltered("Clustering", "CC", "Andamento del Clustering Coefficient (CC) nel tempo")
# plot_metric_unfiltered("APL", "APL", "Andamento dell'Average Path Length (APL) nel tempo")
# plot_metric_unfiltered("Avg Neighbors", "AND", "Andamento dell'Average Neighbors Degree (AND) nel tempo")
# plot_metric_unfiltered("Centralization", "NC", "Andamento della Network Centralization (NC) nel tempo")
# plot_metric_unfiltered("σ", "σ", "Andamento di Sigma σ nel tempo")
# plot_metric_unfiltered("CC", "Connected Components", "Andamento delle Connected Components nel tempo")
