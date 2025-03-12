import pandas as pd
import matplotlib.pyplot as plt

# Percorso del file CSV (modifica se necessario)
csv_file = 'csv-data/all.csv'

# Leggi il CSV
df = pd.read_csv(csv_file)

# Converte la colonna 'Snapshot' in intero (rappresenta l'anno)
df['Snapshot'] = df['Snapshot'].astype(int)

# Converte la colonna "Clustering" in float
# Sostituisce la virgola con il punto per gestire il separatore decimale
df['Clustering'] = df['Clustering'].apply(lambda x: float(str(x).replace(',', '.')))

# Ottieni l'elenco delle categorie univoche
categorie = df['Categoria'].unique()

# Crea il grafico
plt.figure(figsize=(8, 5))
for cat in categorie:
    # Seleziona e ordina i dati per anno della categoria corrente
    subset = df[df['Categoria'] == cat].sort_values(by='Snapshot')
    plt.plot(subset['Snapshot'], subset['Clustering'], marker='o', label=cat)

plt.xlabel('Anno (Snapshot)')
plt.ylabel('Clustering Coefficient')
plt.title('Andamento del Clustering Coefficient nel tempo')
plt.legend(title='Categoria')
plt.grid(True)
plt.tight_layout()
plt.show()
