import Utili
import Nuova_partita
import Fine_partita

import telebot
import json
import datetime
import time
"""
TODO:
-finepartita
    .calcolare ed aggiornare i fondi
-nuovapartita                       *
    .inserire i moltiplicatori
    .inviare a tutti

-puntata
    .mostrare cosa devo puntare
    .possibilità di puntare
    .se punto non posso cambiare
-andamento generale(generale)       *
-andamento personale(personale)     *
"""

API_TOKEN = '2032364818:AAFw5roE8v4S_Sbb7KzgVyRfLLKdcqRTjcg'

bot = telebot.TeleBot(API_TOKEN)


def isConnected(file, id):
    # se l'id è collegato ad una persona
    if str(id) in file['lista_id'].keys():
        return True
    else:
        return False


def chiSono(message, id, file):
    nome_persona = message.text.upper()
    # la persona fa parte della classe?
    if nome_persona in file['persone'].keys():
        if file['persone'][nome_persona]['id'] == 0:  # l'id è vuoto?
            # collego l'id al nome
            file['persone'][nome_persona]['id'] = id
            file['lista_id'].update({str(id): nome_persona})

            Utili.inserisciFile('persone.json', file)
            bot.send_message(id, 'Mi ricorderò di te!')
        elif str(id) in file['lista_id'].keys():    # l'id era già presente?
            bot.send_message(id, '''
            Mi ero dimenticato di te ma ti ho già conosciuto''')
        else:  # stessa persona con due account differenti
            bot.send_message(id, '''
            Qualcuno ha già preso il tuo posto(
            Contatta Leonardo perchè non aveva
            voglia di fare una funzione in cui
            risolveva anche questo problema)''')
    else:
        bot.send_message(id, 'Non credo che tu faccia parte della classe')


while True:

    @bot.message_handler(commands=['start'])
    def nuova_persona(message):
        id = message.from_user.id
        file = Utili.apriFile('persone.json')
        bot.reply_to(message, 'Ciao! Non ti ho mai visto. Chi sei?')
        nomi = []
        for nome in file['persone'].keys():
            nomi.append(nome)
        bot.send_message(id, '\n'.join(nomi))
        bot.register_next_step_handler_by_chat_id(id, chiSono, id, file)

    @bot.message_handler(commands=['andamento'])
    def stampa_andamento(message):
        id = message.from_user.id
        file = Utili.apriFile('persone.json')
        persona = file['lista_id'][str(id)]
        info_persona = file['persone'][persona]
        if isConnected(file, id):
            bot.reply_to(message, f'''
*FONDI ATTUALI:* {info_persona['fondi']}
*PERDITA/GUADAGNO:* {info_persona['guadagno']}
*ANDAMENTO:* {' ➡️ '.join(info_persona['andamento'])}''',
                         parse_mode='Markdown')
        else:
            bot.reply_to(message, 'Prima digita /start e fammi sapere chi sei')

    @bot.message_handler(commands=['generale'])
    def stampa_generale(message):
        id = message.from_user.id
        file = Utili.apriFile('persone.json')
        if isConnected(file, id):
            testo = ''
            for i in file['persone'].keys():
                testo = f'''
{testo}
{i}: *{file['persone'][i]['fondi']}€* | Guadagno: {file['persone'][i]['guadagno']}'''
            bot.reply_to(message, testo, parse_mode='Markdown')
        else:
            bot.reply_to(message, 'Prima digita /start e fammi sapere chi sei')

    @bot.message_handler(commands=['nuovapartita'])
    def nuova_partita(message):
        id = message.from_user.id
        file = Utili.apriFile('persone.json')
        if isConnected(file, id):
            Nuova_partita.start(bot, id)

    @bot.message_handler(commands=['finepartita'])
    def fine_partita(message):
        id = message.from_user.id
        file = Utili.apriFile('persone.json')
        partite = Utili.apriFile('partita.json')
        if isConnected(file, id) and len(partite['attive']) > 0:
            Fine_partita.start(bot, id)
        else:
            bot.send_message(id, 'Non ci sono partite attive')
    bot.polling()
