import telebot
import os
from src.data_handler import get_poll_data
from src.database_handler import create_table, query_data, get_table_list
import logging
import yaml

script_directory = os.path.dirname(os.path.realpath(__file__))

with open(script_directory + "/config.yaml", "r") as stream:
    try:
        config_file = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

options = config_file['options']
whitelisted_ids = config_file['whitelisted_ids']

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

def load_token():
    if config_file['TOKEN'] != 'QUI_IL_TUO_TOKEN':
        TOKEN = config_file['TOKEN']
        return str(TOKEN)

    else:
        TOKEN = os.getenv('TOKEN')
        return str(TOKEN)

def initialize_folder_structure(): ### create data folder if it's not there
    if os.path.isdir(script_directory + '/data'):
        return
    else:
        os.mkdir(script_directory + '/data')
        return

bot = telebot.TeleBot(load_token())

################################## categorie

cat1 = ' - Il ridere'
cat2 = ' - Il sapere'
cat3= ' - Il sacrificio'

##################################

class whitelist_user(telebot.custom_filters.SimpleCustomFilter):
    key='whitelisted_user'
    @staticmethod
    def check(message: telebot.types.Message):
        if str(bot.get_chat_member(message.chat.id,message.from_user.id).user.id) in whitelisted_ids:
            return True

@bot.message_handler(whitelisted_user=True, commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 'Non ammazzate il mio padrone @luke_go se non funziono come dovrei pls.\n<b>Al momento solo LVI può inviarmi i comandi.</b>\n' +
                           'Il database verrà salvato nella cartella: %s'%(script_directory + "/data"), parse_mode='HTML')

@bot.message_handler(whitelisted_user=True, commands=['new_session'])
def new_session(message):
    message = bot.reply_to(message, "Inserisci la data di oggi (DD-MM-YYYY). Potrei farlo manualmente ma se la partita dura oltre la mezzanotte... implodo!")
    bot.register_next_step_handler(message, get_table_name)

def get_table_name(message):
    input = message.text
    bot.reply_to(message, 'Data correttamente inserita: ' + input)
    global date_session
    date_session = str(input).replace('-', '')
    create_table(date_session)

@bot.message_handler(whitelisted_user=True, commands=['vote'])
def send_poll(message):
    message = bot.send_message(message.chat.id, 'Nome relatorə:')
    bot.register_next_step_handler(message, get_user_input)

def send_polls(input, message):
    q1 = bot.send_poll(message.chat.id, input + cat1, options, open_period=60, is_anonymous=True)
    q2 = bot.send_poll(message.chat.id, input + cat2, options, open_period=60, is_anonymous=True)
    q3 = bot.send_poll(message.chat.id, input + cat3, options, open_period=60, is_anonymous=True)

@bot.message_handler(whitelisted_user=True, commands=['save'])
def send_save(message):
    bot.reply_to(message, 'N° voti castati: ' + str(get_poll_data(date_session, message.reply_to_message)), disable_notification=True)
    
@bot.message_handler(whitelisted_user=True, commands=['results'])
def send_results(message):
    generale = "\n".join(query_data(date_session)[0])
    ridere = "\n".join(query_data(date_session)[1])
    sapere = "\n".join(query_data(date_session)[2])
    sacrificio = "\n".join(query_data(date_session)[3])
    bot.reply_to(message, "\n*Classifica generale:*\n%s\n\n*Classifica 'Il ridere':*\n%s\n\n*Classifica 'Il sapere':*\n%s\n\n*Classifica 'Il sacrificio':*\n%s"%(generale, ridere, sapere, sacrificio), parse_mode='MARKDOWN')
    db = open(script_directory + "/data/score_presentazioni.db", 'rb')
    bot.send_document(message.chat.id, db, caption='Questo è il database con i dati. Lo puoi aprire con un qualunque software che supporti SQLite. Io consiglio [DB Browser for SQLite](https://sqlitebrowser.org/).', 
            parse_mode='MARKDOWN')

@bot.message_handler(whitelisted_user=True, commands=['old_session_results'])
def send_old_results(message):
    table_list= get_table_list()
    for i in range (len(table_list)):
        table_list[i] = "<code>" + str(table_list[i]) + "</code>"
        
    message = bot.send_message(message.chat.id, "<b>Data della partita?\nFormato: DD-MM-YYYY</b>\n\nSe non la ricordi... Ecco l'elenco completo:\n" + "\n".join(table_list), parse_mode="HTML")
    bot.register_next_step_handler(message, get_old_table_name)

def get_old_table_name(message):
    input = message.text
    date_session = str(input).replace('-', '')
    generale = "\n".join(query_data(date_session)[0])
    ridere = "\n".join(query_data(date_session)[1])
    sapere = "\n".join(query_data(date_session)[2])
    sacrificio = "\n".join(query_data(date_session)[3])
    bot.reply_to(message, "\n*Classifica generale:*\n%s\n\n*Classifica 'Il ridere':*\n%s\n\n*Classifica 'Il sapere':*\n%s\n\n*Classifica 'Il sacrificio':*\n%s"%(generale, ridere, sapere, sacrificio), parse_mode='MARKDOWN')

@bot.message_handler(commands=['help'])
def send_help(message):
    with open(script_directory + "/src/help.txt","r") as f:
        string = f.read()
    bot.reply_to(message, string, parse_mode='HTML')

@bot.message_handler(commands=['backup'])
def send_database_backup(message):
    db = open(script_directory + "/data/score_presentazioni.db", 'rb')
    bot.send_document(message.chat.id, db, caption='Questo è il database con i dati. Lo puoi aprire con un qualunque software che supporti SQLite. Io consiglio [DB Browser for SQLite](https://sqlitebrowser.org/).', 
            parse_mode='MARKDOWN')

def get_user_input(message):
    input = str(message.text)
    send_polls(input, message)

def main():
    initialize_folder_structure()
    bot.add_custom_filter(whitelist_user()) ### enable USER IDs filter
    bot.infinity_polling(skip_pending=True)

if __name__ == '__main__':
    main()
