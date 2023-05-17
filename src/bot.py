import telebot.types as types
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

# keyboard = types.ReplyKeyboardMarkup(True, True)
# keyboard.add(as_message(CommandType.Project))
# keyboard.add(as_message(CommandType.MediaSupport))
# keyboard.add(as_message(CommandType.Appeal))
# keyboard.add(as_message(CommandType.Discounts))

inline_keyboard = types.InlineKeyboardMarkup(
    [
        [as_inline_button(CommandType.Project)],
        [as_inline_button(CommandType.MediaSupport)],
        [as_inline_button(CommandType.Appeal)],
        [as_inline_button(CommandType.Discounts)]
    ],
    1
)


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message: types.Message):
    bot.send_message(message.chat.id, msg.start, reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda x: True)
def callback(cb: types.CallbackQuery):
    if cb.data in (cmd_type.name for cmd_type in CommandType):
        cmd_type = CommandType[cb.data]
        handler_for(cmd_type)(cb.message)
        bot.answer_callback_query(cb.id)


@message_handler(bot, CommandType.Project)
def new_project(message: types.Message):
    bot.send_message(message.chat.id, "Йо, новий проєкт?")


@message_handler(bot, CommandType.MediaSupport)
def new_project(message: types.Message):
    bot.send_message(message.chat.id, 'Потрібна моя підтримка?')


bot.infinity_polling()
