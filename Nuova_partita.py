import Utili


def inviaMessaggioGlobale(nome):
    file = Utili.apriFile('persone.json')
    for i in file['persone'].keys():
        id = file['persone'][i]['id']
        bot.send_message(id, f'AGGIUNTA PARTITA[{nome}]')


def aggiungiMoltiplicatori(message, id, nome, partite, posizione):

    try:
        n1, nx, n2 = message.text.split(',')
        partite['attive'].append([n1])
        partite['attive'][posizione].append(nx)
        partite['attive'][posizione].append(n1)
        partite['attive'][posizione].append(nome)
        Utili.inserisciFile('partita.json', partite)
        bot.send_message(id, "FATTO!")
        inviaMessaggioGlobale(nome)
    except(ValueError):
        bot.send_message(id, 'Separa con le virgole per favore')


def aggiungiPartita(message, id):
    partite = Utili.apriFile('partita.json')
    nome = message.text
    bot.reply_to(message, 'Aggiungi i moltiplicatori')
    posizione = len(partite['attive'])
    bot.register_next_step_handler_by_chat_id(id,
                                              aggiungiMoltiplicatori,
                                              id, nome, partite, posizione)


def start(b, id):
    global bot
    bot = b
    bot.send_message(id, 'Che partita vuoi aggiungere?')
    bot.register_next_step_handler_by_chat_id(id, aggiungiPartita,
                                              id)
