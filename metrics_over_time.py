import pandas as pd
import matplotlib.pyplot as plt

# Legge il file CSV
df = pd.read_csv("data.csv")

metric = "Centralization"

# Filtra le righe con Categoria "unfiltered"
df_unfiltered = df[df["Categoria"] == "unfiltered"]

# Converte la colonna Snapshot in interi (se necessario)
df_unfiltered["Snapshot"] = df_unfiltered["Snapshot"].astype(int)

# Converte la colonna "Centralization" da stringa (con virgola) a float
df_unfiltered[metric] = (
    df_unfiltered[metric].astype(str).str.replace(",", ".").astype(float)
)

# Ordina il DataFrame per anno
df_unfiltered = df_unfiltered.sort_values(by="Snapshot")

# Crea il grafico
plt.figure(figsize=(10, 6))
plt.plot(
    df_unfiltered["Snapshot"],
    df_unfiltered[metric],
    marker="o",
    linestyle="-",
    color="blue",
)
plt.title("Andamento della Centralizzazione")
plt.xlabel("Anno")
plt.ylabel("Centralizzazione")
plt.grid(True)
plt.show()
