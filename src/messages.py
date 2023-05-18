from commands import CommandType

start = '''Вітаємо, це бот для пропозицій до співпраці з УСЛ.

Тут ви зможете запропонувати нам пропозицію до співпраці, проєкт або ж запросити медійну підтримку. 

Творимо кращий час разом!'''


commands = {
    CommandType.Project: [
        'Надайте короткий опис проєкту (5-10 речень).',

        'Сформулюйте ціль проєкту (2-3 речення).',

        'Опишіть необхідні ресурси УСЛу, які потрібні Вам для реалізації проєкту.\n'
        'Наприклад: юридична консультація, допомога відділу HR, '
        'допомога у залученні інших університетів, фінансування, залучення людей до організації проєкту.',

        'Точки дотику з УСЛ, чому проєкт є корисним для вас та спільноти УСЛ?\n'
        'Наприклад: спільна медійна компанія, залученість колегіантів у ролі спікерів і тд.'
    ],
    CommandType.MediaSupport: [
        'Якого роду медійну співпрацю ви хочете запропонувати?',
        'Надішліть посилання на додаткову інформацію та матеріали для поширення',
    ],
    CommandType.Appeal: [
        "Напишіть свої думки про УСЛ, ми обов'язково Вас почуємо :)."
    ]
}

_command_chat_message = {
    CommandType.Project:
        '''запропонував новий проєкт.
        
_Опис проєкту:_
*{}*

_Ціль проєкту:_
*{}*

_Необхідні ресурси:_
*{}*

_Точки дотику з УСЛ:_
*{}*''',
    CommandType.MediaSupport:
        '''запропонував медійну підтримку.
        
*{}*

_Додаткова інформація:_
*{}*''',
    CommandType.Appeal:
        '''залишив звернення:
        
*{}*''',
    CommandType.Discounts: "зробив запит на знижки для студентів."
}


def chat_message(cmd_type: CommandType) -> str:
    message: str = "Користувач @{} "
    if cmd_type in _command_chat_message:
        message += _command_chat_message[cmd_type]
    return message


command_end = 'Дякуємо, ми розглянемо вашу заявку та невдовзі ви отримаєте відповідь.'
