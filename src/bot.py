import telebot.types as types
from telebot import TeleBot

import config
import messages as msg
import utils
from user import User
import auth
from commands import *

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


@bot.message_handler(commands=['help'])
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
    bot.send_message(chat_id, 'Зовсім скоро тут зʼявляться унікальні можливості саме для тебе:)')


def start_processing_command(chat_id: int, cmd_type: CommandType):
    if cmd_type not in msg.commands or not msg.commands[cmd_type]:
        send_not_implemented(bot, chat_id)
        return
    questions = msg.commands[cmd_type]
    answers: list[str] = []
    first_question_idx: int = 0
    ask_question(chat_id, questions, first_question_idx, answers, cmd_type)


def ask_question(chat_id: int, questions: list[str], i_question: int, answers: list[str], cmd_type: CommandType):
    bot.send_message(chat_id, questions[i_question])
    bot.register_next_step_handler_by_chat_id(chat_id, process_answer, questions, i_question + 1, answers, cmd_type)


def process_answer(message: types.Message, questions: list[str], i_next_question: int, answers: list[str],
                   cmd_type: CommandType):
    answers.append(message.text)
    if i_next_question < len(questions):
        ask_question(message.chat.id, questions, i_next_question, answers, cmd_type)
    else:
        answer = msg.command_end
        bot.send_message(message.chat.id, answer, reply_markup=inline_keyboard)
        utils.send_message_to_my_chat(bot, utils.answers_str(answers, cmd_type, message.from_user))


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


@bot.message_handler(commands=['start'])
def authorize(message: types.Message):
    authorized_user = auth.get_authorized_user(message.from_user.id)
    if authorized_user is not None:
        welcome_message(message)
    else:
        bot.send_message(message.chat.id, msg.invitation)
        bot.register_next_step_handler_by_chat_id(message.chat.id, save_user_info)


def save_user_info(message: types.Message):
    user = User(id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name,
                description=message.text)
    auth.authorize(user)
    welcome_message(message)


bot.infinity_polling()
