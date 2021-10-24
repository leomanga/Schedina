import Utili


def ottieniVincitore(message, id, file_partite, numero):
    # 1->0; X->1; 2->2 in lista
    vincitore = None
    if message.text.upper() == '1':
        vincitore = 0
    elif message.text.upper() == 'X':
        vincitore = 1
    elif message.text.upper() == '2':
        vincitore = 2
    else:
        bot.send_message(id, 'Qualcosa non torna')
        return

    partita_finita = file_partite['attive'][numero]
    file_persone = Utili.apriFile('persone.json')
    for i in file_persone['persone'].keys():
        id_persona = file_persone['persone'][i]['id']
        puntata = file_persone['persone'][i]['ultima puntata'].pop(numero)

        vincita = puntata[vincitore] * partita_finita[vincitore]
        guadagno = vincita - sum(puntata)
        file_persone['persone'][i]['fondi'] = file_persone['persone'][i]['fondi'] + guadagno
        file_persone['persone'][i]['andamento'].append(file_persone['persone'][i]['fondi'])
        file_persone['persone'][i]['guadagno'] = file_persone['persone'][i]['fondi'] - 1000
        bot.send_message(id_persona,
                         f"E' finita la partita[{file_partite['attive'][numero]}]\nGuadagno: {guadagno}")

    file_partite['attive'].pop(numero)
    Utili.inserisciFile('partita.json', file_partite)
    Utili.inserisciFile('persone.json', file_persone)


def eliminaPartita(message, id, file):
    try:
        numero = int(message.text)-1
        bot.send_message(id, 'Chi ha vinto?(scrivi 1, X o 2)')
        bot.register_next_step_handler_by_chat_id(id, ottieniVincitore,
                                                  id, file, numero)
    except(ValueError):
        bot.send_message(id, 'Qualcosa non mi torna')


def start(b, id):
    global bot
    bot = b
    bot.send_message(id, 'Che partita vuoi eliminare(digita il numero)?')
    file = Utili.apriFile('partita.json')
    testo = ''
    i = 1
    for partita in file['attive']:
        testo = f'{testo}{i}) {partita[3]}\n'
        i += 1
    bot.send_message(id, testo)
    bot.register_next_step_handler_by_chat_id(id, eliminaPartita,
                                              id, file)
