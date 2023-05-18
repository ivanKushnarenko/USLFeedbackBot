from commands import CommandType
import config
import messages as msg


def answers_str(answers: list[str], cmd_type: CommandType, username: str) -> str:
    return msg.chat_message(cmd_type).format(username, *answers)


def send_message_to_my_chat(bot, message_text: str):
    bot.send_message(config.CHAT_ID, message_text, parse_mode='markdown')
