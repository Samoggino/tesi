from collections import defaultdict

def process_channels(cln_channels):
    channel_dict = defaultdict(lambda: {
        "node1_pub": None,
        "node2_pub": None,
        "max_capacity_msat": 0,
        "last_update": 0
    })
    
    # Aggiungi un contatore per monitorare quale canale viene elaborato
    channel_counter = 0

    for channel in cln_channels:
        channel_counter += 1  # Incrementa il contatore ad ogni iterazione
        print(f"Elaborando canale numero {channel_counter}...")  # Stampa il numero del canale
        
        # Se il canale è una lista, iteriamo su ciascun elemento
        if isinstance(channel, list):
            for sub_channel in channel:
                if isinstance(sub_channel, dict):  # Se l'elemento è un dizionario, procediamo
                    process_single_channel(sub_channel, channel_dict, channel_counter)
                else:
                    print(f"Canale {channel_counter} non è un dizionario valido! Ignorato. Valore del canale: {sub_channel}")
            continue  # Passa al prossimo canale
        
        # Se il canale non è una lista, lo trattiamo come un singolo canale
        elif isinstance(channel, dict):
            process_single_channel(channel, channel_dict, channel_counter)
        else:
            print(f"Canale {channel_counter} non è un dizionario valido! Ignorato. Valore del canale: {channel}")
            continue  # Ignora se il canale non è un dizionario valido

    # Aggiungi un controllo finale per verificare quanti canali validi sono stati processati
    print(f"Totale canali validi elaborati: {len(channel_dict)}")
    return channel_dict

def process_single_channel(channel, channel_dict, channel_counter):
    scid_raw = channel.get("scid", "")
    if not scid_raw:
        print(f"Attenzione: Canale {channel_counter} senza SCID! {channel}")
        return  # Ignora il canale senza SCID

    if isinstance(scid_raw, list):
        print(f"Attenzione: SCID è una lista! Valore: {scid_raw} Canale: {channel_counter}")
        return  # Salta il canale perché il formato non è chiaro
    
    # Prendi la parte di SCID prima del "/"
    scid_clean = scid_raw.split("/")[0] if isinstance(scid_raw, str) else str(scid_raw)
    
    # Controlla se i nodi sono presenti
    node1 = channel.get("source", "").strip()
    node2 = channel.get("destination", "").strip()

    if not node1 or not node2:
        print(f"Attenzione: Canale {channel_counter} con nodi mancanti! {channel}")
        return

    # Ordina i nodi
    if node1 > node2:
        node1, node2 = node2, node1

    # Popola il dizionario dei canali se non esiste già
    if channel_dict[scid_clean]["node1_pub"] is None:
        channel_dict[scid_clean]["node1_pub"] = node1
        channel_dict[scid_clean]["node2_pub"] = node2

    # Gestione della capacità massima
    htlc_maximum_msat = channel.get("htlc_maximum_msat", 0)
    if htlc_maximum_msat:
        channel_dict[scid_clean]["max_capacity_msat"] = max(
            channel_dict[scid_clean]["max_capacity_msat"],
            htlc_maximum_msat
        )

    # Gestione del timestamp
    timestamp = channel.get("timestamp", 0)
    if timestamp > channel_dict[scid_clean]["last_update"]:
        channel_dict[scid_clean]["last_update"] = timestamp
