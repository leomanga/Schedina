import json


def apriFile(nome_file):
    with open(nome_file) as f:
        dati = json.load(f)
        f.close()
        return dati


def inserisciFile(nome_file, dati):
    with open(nome_file, 'w') as f:
        json.dump(dati, f)
        f.close()
