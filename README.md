## Prima configurazione

1) Nel file ```config.yaml``` inserisci il token del tuo bot che hai creato con [@BotFather](https://t.me/BotFather).

	TOKEN: QUI_IL_TUO_TOKEN

 Se preferisci, puoi anche inserire il TOKEN utilizzando l'environment varibale ```API_TOKEN```. 

2) Nel file ```config.yaml``` inserisci l'elenco degli ```USER ID``` (puoi ottenerlo chattando con [@getmyid_bot](https://t.me/getmyid_bot)) che saranno autorizzati a usare i comandi del bot.

Il formato da seguire è:
```
- 'USER_ID_1'
- 'USER_ID_2'
- 'USER_ID_3'
```

Ovviamente tutti gli utenti appartenteneti al gruppo potranno sempre votare senza alcuna altra operazione necessaria.

#### Logging

Se vuoi disattivare il logging, commenta le righe 21 e 22 aggiungendo un "```#```":

Da così:

```
logger = telebot.logger

telebot.logger.setLevel(logging.DEBUG)
```
A così: 

```
#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)
```

## Avvio del bot 

#### Docker

In alternativa al metodo descritto sopra, puoi utlizzare Docker:

```docker compose up```

Fatto.

#### Non so usare Docker

1) Installa Python e Pip sul tuo PC

2) Installa i moduli necessari al funzionamento del bot con il comando:

```pip install -r requirements.txt```

3) Avvia il bot con il comando:

```pyhton main.py```

Si consiglia l'utilizzo di un [virtual environment](https://towardsdatascience.com/virtual-environments-104c62d48c54).

### Attualmente supporto i comandi:

```/start``` - beh starta il bot

```/new_session``` - avvia una nuova serata PowerPoint

```/vote``` - avvia una nuova votazione

```/save ```- salva i risultati della votazione

```/results``` - visualizza i risultati della partita odierna

```/old_session_results``` - visualizza i risultati di una partita precedente

```/backup``` - ottieni la copia del database delle serate PowerPoint

```/help``` - ti spiego come funziono

## Avvio nuova serata PowerPoint

<b>1)</b> All'inizio di una serata PowerPoint dammi il comando ```/new_session``` per iniziare una nuova partita. Ti verrà richiesto di inserire la data odierna nel formato <code>DD-MM-YYYY.</code>

<b>2)</b> Alla fine di ogni presentazione dammi il comando ```/vote```, ti chiederò il nome del relatore e dopo invierò 3 sondaggi relativi alle 3 categorie per le quali state competendo:

1) Il ridere
2) Il sapere
3) Il sacrificio

La presentazione del giorno sarà quella che avrà totalizzato più punti sommando quelli ottenuti nelle categorie "Il ridere" e "Il sapere".

<b>DOPO</b> la conclusione delle votazioni, rispondi a **ciascun sondaggio** inviando il comando ```/save``` per memorizzarne il risultato.

<b>3)</b> Ripeti il punto 2) per ogni relatore.

<b>4)</b> Quando tutti hanno esposto la propria relazione, dammi il comando ```/results``` per visualizzare le classifiche finali e decretare il vincitore.

<b>5)</b> Se vuoi vedere il risultato di una vecchia partita, dammi il comando ```/old_session_results```.

<b>6)</b> Ottieni la copia del database delle serate PowerPoint ```/backup```.  Lo puoi aprire con un qualunque software che supporti SQLite. Io consiglio [DB Browser for SQLite](https://sqlitebrowser.org/).

<i>Perché c'è un mix di inglese e italiano? Boh.</i> 🎲️
