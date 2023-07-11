import os
from typing import Optional

import telebot.types

import auth
import config
import messages as msg
from commands import CommandType
from user import User


def _answers_str(answers: list[str], cmd_type: CommandType, user: telebot.types.User) -> str:
    username: Optional[str] = '@' + user.username if user.username else user.full_name
    user_ref: str = f'[{username}](tg://user?id={user.id})'
    res: str = msg.chat_message(cmd_type).format(user_ref, *answers)
    authorized_user: User = auth.get_authorized_user(user.id)
    if authorized_user and authorized_user.description:
        res += f'\n\n_Автор звернення:_\n*{authorized_user.description}*'
    return res


def send_answers(bot, answers: list[str], cmd_type: CommandType, from_user: telebot.types.User):
    send_message_to_my_chat(bot, _answers_str(answers, cmd_type, from_user))


def send_message_to_my_chat(bot, message_text: str):
    bot.send_message(os.getenv('MY_CHAT_ID'), message_text, parse_mode='markdown')
