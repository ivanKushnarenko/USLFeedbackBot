import telebot.types as types
from telebot import TeleBot

from commands import *


import config
import messages as msg
import utils

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
    if cb.data not in (cmd_type.name for cmd_type in CommandType):
        pass
    else:
        cmd_type = CommandType[cb.data]
        handler_for(cmd_type)(cb.message)
        bot.answer_callback_query(cb.id)


def send_not_implemented(bot: TeleBot, chat_id: int):
    bot.send_message(chat_id, 'Поки що не зроблено:(')


def start_processing_command(chat_id: int, cmd_type: CommandType):
    if cmd_type not in msg.commands:
        send_not_implemented(bot, chat_id)
    questions = msg.commands[cmd_type]
    answers: list[str] = []
    if len(questions):
        ask_question(chat_id, questions, 0, answers)
    else:
        send_not_implemented(bot, chat_id)


def ask_question(chat_id: int, questions: list[str], i: int, answers: list[str]):
    bot.send_message(chat_id, questions[i])
    bot.register_next_step_handler_by_chat_id(chat_id, process_answer, questions, i + 1, answers)


def process_answer(message: types.Message, questions: list[str], i: int, answers: list[str]):
    answers.append(message.text)
    if i < len(questions):
        ask_question(message.chat.id, questions, i, answers)
    else:
        answer = msg.command_end + utils.answers_str(answers)
        bot.send_message(message.chat.id, answer)


@message_handler(bot, CommandType.Project)
def new_project(message: types.Message):
    start_processing_command(message.chat.id, CommandType.Project)


@message_handler(bot, CommandType.MediaSupport)
def media_support(message: types.Message):
    start_processing_command(message.chat.id, CommandType.MediaSupport)


@message_handler(bot, CommandType.Appeal)
def appeal(message: types.Message):
    start_processing_command(message.chat.id, CommandType.Appeal)


@message_handler(bot, CommandType.Discounts)
def discounts(message: types.Message):
    start_processing_command(message.chat.id, CommandType.Discounts)


bot.infinity_polling()
