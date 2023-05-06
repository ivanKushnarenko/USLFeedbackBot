from telebot import TeleBot

import config
import messages as msg

bot = TeleBot(config.API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def welcome_message(message):
    bot.send_message(message.chat.id, msg.start)


bot.infinity_polling()
