import telebot.types
from telebot import TeleBot


import config
import messages as msg

bot = TeleBot(config.API_TOKEN)

bot.delete_my_commands()
bot.set_my_commands([
    telebot.types.BotCommand('/project', 'Запропонувати проєкт'),
    telebot.types.BotCommand('/media_support', 'Медійна підтримка'),
    telebot.types.BotCommand('/appeal', 'Залишити відгук/скаргу/звернення'),
    telebot.types.BotCommand('/discounts', 'Знижки студентам'),
    telebot.types.BotCommand('/help', 'Що вміє цей бот')
])


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    bot.send_message(message.chat.id, msg.start)


bot.infinity_polling()
