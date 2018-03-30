import sys
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import telegram
from telegram import KeyboardButton
from loc import get_lat_lng
from questionparser import QuestionParser

# from chatterbot import ChatBot
# chatbot = ChatBot(
#     'Ron Obvious',
#     trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
# )

# chatbot.train("chatterbot.corpus.english")

# initiate bot
try:
    with open('token.txt', 'r') as f:
        TOKEN = f.readline().strip()
except IOError:
    print("No token file. Please create a token.txt with your token in the first line.")
    sys.exit()

# command function
# command: /start
# output: greeting message
def start(bot, update):
    sender = update.message.chat.first_name
    help_msg = "! How can I help you? Use /info to ask me factoid questions, please!"
    greeting = "Hi, " + sender + help_msg
    bot.send_message(chat_id=update.message.chat_id, text=greeting)

# message function
# output: converse with user
# def courtesy_reply(bot, update):
#     message = update.message.text
#     reply = chatbot.get_response(message)
#     print(reply)
#     update.message.reply_text(reply.text)

# command & message function
# command: /info
# message: a question
# output: question parsing result
def information_reply(bot, update):
    message = update.message.text
    # status_msg = "(Only replying question type and keywords as of now)"
    # bot.send_message(chat_id=update.message.chat_id, text=status_msg)
    question = " ".join(message.split()[1:])
    print(question)
    qp = QuestionParser(question)
    qp.preprocess()
    e_loc = qp.get_loc_entity()
    print(qp.get_type())
    if e_loc and qp.get_type() == 'LOC':
        cood = get_lat_lng(" ".join(e_loc))
        bot.sendLocation(chat_id=update.message.chat_id, latitude=cood[0], longitude=cood[1])
    else: update.message.reply_text(qp.get_type())
    

def error_handler(error):
    print("Caught an error", error)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_error_handler(error_handler)
    # chatty = MessageHandler(Filters.text, courtesy_reply)
    # dispatcher.add_handler(chatty)
    info_handler = CommandHandler('info', information_reply)
    dispatcher.add_handler(info_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
