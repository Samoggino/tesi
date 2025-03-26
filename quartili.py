import matplotlib.pyplot as plt
import numpy as np

# Dati: percentuali della capacità totale per ciascun quartile, per ogni grafico
# Ogni lista rappresenta le percentuali per i 4 quartili di un file
quartile_percentages = {
    'totale': [0.35, 3.09, 12.47, 84.08],
    'almeno due canali': [0.55, 4.07, 13.17, 82.21],
    'top10 esclusa': [0.50, 4.29, 14.15, 81.07],
    'top100 esclusa': [0.40, 4.53, 13.29, 81.78],
}

# Creiamo il grafico
labels = ['0-25%', '25-50%', '50-75%', '75-100%']
categories = list(quartile_percentages.keys())

# Prepariamo le posizioni delle barre
x = np.arange(len(labels))  # le posizioni dei quartili
width = 0.15  # larghezza delle barre

# Crea la figura e l'asse
fig, ax = plt.subplots(figsize=(10, 6))

# Aggiungiamo le barre per ogni categoria
for i, category in enumerate(categories):
    ax.bar(x + i * width, quartile_percentages[category], width, label=category)

# Aggiungiamo etichette e altre personalizzazioni
ax.set_xlabel('Segmento dei canali (quartili)')
ax.set_ylabel('Percentuale della capacità totale (%)')
ax.set_title('Distribuzione della liquidità nei canali')
ax.set_xticks(x + width * (len(categories) - 1) / 2)
ax.set_xticklabels(labels)
ax.legend(title="Categorie di nodi")

plt.tight_layout()
plt.show()
