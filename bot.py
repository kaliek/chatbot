from adam_qas.qas.adam import main as adam_main
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

try:
    with open('token.txt', 'r') as f:
        TOKEN = f.readline().strip()
except IOError:
    print("No token file. Please create a token.txt with your token in the first line.")
    sys.exit()

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi, how can I help you!")

def reply(bot, update):
    question = update.message.text
    answer = adam_main([question])
    update.message.reply_text(answer)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    answer = MessageHandler(Filters.text, reply)
    dispatcher.add_handler(answer)
    
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

