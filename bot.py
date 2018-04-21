import sys
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, Filters
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import csv
from questionparser import QuestionParser
from smartanswer import SmartAnswer
from question_answer_rating import add_line
from neuralcoref import Coref
from chatterbot import ChatBot
# chatbot = ChatBot(
#     'Ron Obvious',
#     trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
# )

# chatbot.train("chatterbot.corpus.english")
coref = Coref()

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
def courtesy_reply(bot, update):
    message = update.message.text
    reply = chatbot.get_response(message)
    print(reply)
    update.message.reply_text(reply.text)

# command & message function
# command: /info
# message: a question
# output: question parsing result
def information_reply(bot, update):
    message = update.message.text
    user_id = update.message.chat_id
    # status_msg = "(Only replying question type and keywords as of now)"
    # bot.send_message(chat_id=update.message.chat_id, text=status_msg)
    question = u" ".join(message.split()[1:])
    add_line([user_id, question])
    print(question)
    coref.continuous_coref(utterances=question)
    question = coref.get_resolved_utterances()[0]
    sans = SmartAnswer(question)
    loc = sans.is_loc_answer()
    if loc:
        add_line([user_id, "loc"])
        bot.sendLocation(chat_id=user_id, latitude=loc[0], longitude=loc[1])
    else:
        hum = sans.is_hum_answer()
        if hum: 
            add_line([user_id, "hum"])
            update.message.reply_text(hum)
        else: 
            add_line([user_id, "wiki"])
            wiki = sans.is_wiki_answer()
            if wiki:
                for w in wiki:
                    update.message.reply_text(w) 
            else: 
                update.message.reply_text(sans.get_type())
    like_keyboard = InlineKeyboardButton(text = "Yes!", callback_data = "liked")
    dislike_keyboard = InlineKeyboardButton(text = "No :(", callback_data = "disliked")
    reply_markup = InlineKeyboardMarkup([[like_keyboard, dislike_keyboard]])
    bot.send_message(chat_id=user_id,
                    text="Do you like the answer?",
                    reply_markup=reply_markup)

def save_rating(bot, update):
    rating = update.callback_query
    user_id = rating.message.chat_id
    print(rating.data)
    add_line([user_id, rating.data])
    bot.edit_message_text(text="You {} my answer :O".format(rating.data),
                          chat_id=user_id,
                          message_id=rating.message.message_id)

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
    rate_handler = CallbackQueryHandler(save_rating)
    dispatcher.add_handler(rate_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
