import enum
from enum import Enum

from telebot.types import BotCommand, InlineKeyboardButton


@enum.unique
class CommandType(Enum):
    Project = 1
    MediaSupport = 2
    Appeal = 3
    Discounts = 4
    Help = 5


_commands = {
    CommandType.Project: 'new_project',
    CommandType.MediaSupport: 'media_support',
    CommandType.Appeal: 'appeal',
    CommandType.Discounts: 'discounts',
    CommandType.Help: 'help'
}

_messages = {
    CommandType.Project: 'Запропонувати проєкт',
    CommandType.MediaSupport: 'Медійна підтримка',
    CommandType.Appeal: 'Залишити відгук/скаргу/звернення',
    CommandType.Discounts: 'Знижки студентам',
    CommandType.Help: 'Що вміє цей бот'
}


def as_command(cmd_type: CommandType) -> str:
    return '/' + _commands[cmd_type]


def as_command_text(cmd_type: CommandType) -> str:
    return _commands[cmd_type]


def as_message(cmd_type: CommandType) -> str:
    return _messages[cmd_type]


def as_bot_command(cmd_type: CommandType) -> BotCommand:
    return BotCommand(as_command(cmd_type), as_message(cmd_type))


def as_inline_button(cmd_type: CommandType) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=as_message(cmd_type), callback_data=cmd_type.name)


def message_handler(bot, cmd_type: CommandType):

    def _inner(func):
        decorated_func = \
            bot.message_handler(commands=[as_command_text(cmd_type)])(
                bot.message_handler(func=lambda message: message.text == as_message(cmd_type))(
                    func
                )
            )
        if cmd_type not in message_handler.command_handlers:
            message_handler.command_handlers[cmd_type] = decorated_func
        decorated_func.cmd_type = cmd_type
        return decorated_func

    return _inner


message_handler.command_handlers = {}


def handler_for(cmd_type: CommandType):
    return message_handler.command_handlers[cmd_type]


if __name__ == '__main__':
    print(f'CommandType.Project as command: {as_command(CommandType.Project)}')
    print(f'CommandType.MediaSupport as command text: {as_command_text(CommandType.MediaSupport)}')
    print(f'CommandType.Appeal as message: {as_message(CommandType.Appeal)}')
