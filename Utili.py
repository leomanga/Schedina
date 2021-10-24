import json


def inviaMessaggioGlobale(bot, id,  str):
    file = apriFile('persone.json')
    for i in file['persone'].keys():
        id = file['persone'][i]['id']
        bot.send_message(id, str)


def apriFile(nome_file):
    with open(nome_file) as f:
        dati = json.load(f)
        f.close()
        return dati


def inserisciFile(nome_file, dati):
    with open(nome_file, 'w') as f:
        json.dump(dati, f)
        f.close()
