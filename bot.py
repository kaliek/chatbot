from adam_qas.qas.adam import main as adam_main, init_qas 
from neuralcoref.neuralcoref import Coref
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from chatterbot import ChatBot

chatbot = ChatBot(
    'Ron Obvious',
    trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
)

chatbot.train("chatterbot.corpus.english")
coref = Coref()
qas = init_qas()
try:
    with open('token.txt', 'r') as f:
        TOKEN = f.readline().strip()
except IOError:
    print("No token file. Please create a token.txt with your token in the first line.")
    sys.exit()


def start(bot, update):
    sender = update.message.chat.first_name
    greeting = "Hi, " + sender + "! How can I help you? Use /info to ask me factoid questions, please!"
    bot.send_message(chat_id=update.message.chat_id, text=greeting)

def courtesy_reply(bot, update):
    message = update.message.text
    reply = chatbot.get_response(message)
    print(reply)
    update.message.reply_text(reply.text)

def information_reply(bot, update):
    message = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text="(Only replying question type and keywords as of now)")
    coref.continuous_coref(utterances = message)
    question = coref.get_resolved_utterances()
    print(question)
    answer = adam_main(qas, question)
    update.message.reply_text(answer)

def error_handler(error):
    print("Caught an error", error)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_error_handler(error_handler)
    chatty = MessageHandler(Filters.text, courtesy_reply)
    dispatcher.add_handler(chatty)
    info_handler = CommandHandler('info', information_reply)
    dispatcher.add_handler(info_handler)
    
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

