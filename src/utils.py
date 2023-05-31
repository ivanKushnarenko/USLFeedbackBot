import telebot.types

import auth
import config
import messages as msg
from commands import CommandType
from user import UserInfo


def answers_str(answers: list[str], cmd_type: CommandType, user: telebot.types.User) -> str:
    username: str = user.username
    full_name: str = user.full_name
    user_info: UserInfo = auth.user_info(user.id)
    if user_info is not None:
        username = user_info.username
        full_name = user_info.full_name
    user_ref: str = "@" + username if username else f"[{full_name}](tg://user?id={user.id})"
    res: str = msg.chat_message(cmd_type).format(user_ref, *answers)
    if user_info and user_info.description:
        res += f'\n\n_Автор звернення:_\n*{user_info.description}*'
    return res


def send_message_to_my_chat(bot, message_text: str):
    bot.send_message(config.CHAT_ID, message_text, parse_mode='markdown')
