



def ottieniNome(message, id):



def aggiungiPartita(message, id):
    # se l'ultima partita è 0 vuol dire che non ci sono partite in corso
    partite = Utili.apriFile('partita.json')
    if partite['ultima'] == 0:

        #
    else:
        bot.send_message(id,
                         f'Prima deve finire la partita: {partite["ultima"][3]}')
