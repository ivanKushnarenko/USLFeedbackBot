import enum
from enum import Enum

from telebot.types import BotCommand

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


if __name__ == '__main__':
    print(f'CommandType.Project as command: {as_command(CommandType.Project)}')
    print(f'CommandType.MediaSupport as command text: {as_command_text(CommandType.MediaSupport)}')
    print(f'CommandType.Appeal as message: {as_message(CommandType.Appeal)}')
