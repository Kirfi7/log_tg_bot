import datetime, time
from aiogram import types


_default_buttons = [
    [
        types.KeyboardButton(text="Основные выгрузки")
    ],
    [
        types.KeyboardButton(text="Сформировать топ"),
        types.KeyboardButton(text="Поощрение по топу")
    ]
]
menu = types.ReplyKeyboardMarkup(_default_buttons, resize_keyboard=True)

_main_buttons = [
    [
        types.KeyboardButton(text="Статистика по серверу")
    ],
    [
        types.KeyboardButton(text="Количество логов"),
        types.KeyboardButton(text="Агенты поддержки"),
        types.KeyboardButton(text="Онлайн админов")
    ],
    [
        types.KeyboardButton(text="В главное меню")
    ]
]
main_markup = types.ReplyKeyboardMarkup(_main_buttons, resize_keyboard=True)

_type_buttons = [
    [
        types.KeyboardButton(text="Репорты"),
        types.KeyboardButton(text="Мероприятия"),
        types.KeyboardButton(text="Вопросы")
    ],
    [
        types.KeyboardButton(text="Джаилы"),
        types.KeyboardButton(text="Муты"),
        types.KeyboardButton(text="Кики")
    ],
    [
        types.KeyboardButton(text="В главное меню")
    ]
]
top_markup = types.ReplyKeyboardMarkup(_type_buttons, resize_keyboard=True)

_to_menu_buttons = [
    [
        types.KeyboardButton(text="В главное меню")
    ]
]
to_menu = types.ReplyKeyboardMarkup(_to_menu_buttons, resize_keyboard=True)

_param_buttons = [
    [
        types.KeyboardButton(text="500 100"),
        types.KeyboardButton(text="750 150")
    ],
    [
        types.KeyboardButton(text="В главное меню")
    ]
]
param_markup = types.ReplyKeyboardMarkup(_param_buttons, resize_keyboard=True)


def get_keyboard():
    now_date = datetime.date.today()
    yesterday = now_date - datetime.timedelta(days=1)
    month1, day1 = str(now_date).split("-")[1:]
    month0, day0 = str(yesterday).split("-")[1:]

    buttons = [
        [
            types.KeyboardButton(text=f"{day1}.{month1}"),
            types.KeyboardButton(text=f"{day0}.{month0}")
        ],
        [
            types.KeyboardButton(text="В главное меню")
        ]
    ]
    return types.ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_logs_keyboard():
    date1 = datetime.date.today() - datetime.timedelta(days=datetime.date.today().isoweekday()-1)
    date2 = date1 - datetime.timedelta(weeks=1)
    m1, d1 = str(date1).split("-")[1:]
    m2, d2 = str(date2).split("-")[1:]
    buttons = [
        [
            types.KeyboardButton(text=f"{d1}.{m1}"),
            types.KeyboardButton(text=f"{d2}.{m2}")
        ],
        [
            types.KeyboardButton(text="В главное меню")
        ]
    ]
    return types.ReplyKeyboardMarkup(buttons, resize_keyboard=True)
