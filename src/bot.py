import telebot
from telebot.types import ReplyKeyboardMarkup
from telebot import TeleBot

from commands import *


import config
import messages as msg

bot = TeleBot(config.API_TOKEN)

bot.delete_my_commands()
bot.set_my_commands([
    as_bot_command(CommandType.Project),
    as_bot_command(CommandType.MediaSupport),
    as_bot_command(CommandType.Appeal),
    as_bot_command(CommandType.Discounts),
    as_bot_command(CommandType.Help)
])

keyboard = ReplyKeyboardMarkup(True, True)
keyboard.add(as_message(CommandType.Project))
keyboard.add(as_message(CommandType.MediaSupport))
keyboard.add(as_message(CommandType.Appeal))
keyboard.add(as_message(CommandType.Discounts))


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    bot.send_message(message.chat.id, msg.start, reply_markup=keyboard)


bot.infinity_polling()
