import py4cytoscape as py4

# Controlla la connessione a Cytoscape
py4.cytoscape_ping()
py4.cytoscape_version_info()

# Ottieni la lista delle reti disponibili in Cytoscape
networks = py4.get_network_list()
print("Reti disponibili:", networks)

# Seleziona la rete da modificare
network_id = networks[1]  # Assumendo che ci sia almeno una rete
py4.set_current_network(network_id)

# Ottieni i nomi delle colonne nella tabella dei nodi
node_columns = py4.tables.get_table_column_names(table='node')
print("Colonne nella tabella dei nodi:", node_columns)

# Imposta la mappatura della dimensione del nodo in base al grado
degree_values = py4.get_table_column_data(table='node', column='Degree')
if all(value is not None for value in degree_values):
    py4.style_mappings.set_node_size_mapping(
        table_column='Degree',
        mapping_type='c',  # 'c' per mappatura continua
        style_name='default'
    )
else:
    print("La colonna 'Degree' contiene valori mancanti.")


# Applica il layout "force-directed" con parametri personalizzati
py4.layout_network("force-directed", 
                   defaultSpringCoefficient=0.000001,  # Minore valore = meno attrazione
                   defaultSpringLength=1000,           # Maggiore valore = nodi più distanti
                   defaultNodeMass=1000) 

# Applica il layout "force-directed"
py4.layout_network("force-directed")

print("Layout applicato con successo!")