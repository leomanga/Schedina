import Utili


def eliminaPartita(message, id, file):
    try:
        numero = int(message.text)
        file['attive'][0][numero].pop(numero-1)
        Utili.inserisciFile('partita.json', file)
    except Exception as e:
        print(e)


def start(b, id):
    global bot
    bot = b
    bot.send_message(id, 'Che partita vuoi eliminare(digita il numero)?')
    file = Utili.apriFile('partita.json')
    testo = ''
    i = 1
    for partita in file['attive']:
        print(partita)
        testo = f'{testo}{i}) {partita[3]}\n'
        i += 1
    bot.send_message(id, testo)
    bot.register_next_step_handler_by_chat_id(id, eliminaPartita,
                                              id, file)
