import py4cytoscape as py4
import time

# Controlla la connessione a Cytoscape
py4.cytoscape_ping()
py4.cytoscape_version_info()

# Ottieni la lista delle reti disponibili in Cytoscape
networks = py4.get_network_list()
print("Reti disponibili:", networks)

## obiettivo: eseguire analyze_network di cytoscape
# Seleziona la rete da modificare
network_id = networks[2]  # Assumendo che ci sia almeno una rete
py4.set_current_network(network_id)

# Avvia il timer
start_time = time.time()

# Esegui l'analisi della rete
analysis_results = py4.analyze_network()

# Mostra i risultati dell'analisi
print("⚡ Lightning Network Analysis ⚡")
for key, value in analysis_results.items():
    print(f"{key}: {value}")

# Tempo di analisi
print(f"Analysis time (sec): {time.time() - start_time}")