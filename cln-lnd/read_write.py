import json

# Funzione per leggere il file JSON di input
def read_input_json(input_file):
    with open(input_file, 'r') as f:
        return json.load(f)

# Funzione per scrivere il file JSON di output
def write_output_json(output_file, data):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
