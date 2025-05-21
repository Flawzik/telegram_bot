from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


prof = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data='btn1'),
            InlineKeyboardButton(text='2', callback_data='btn2')
        ],
        [
            InlineKeyboardButton(text='3', callback_data='btn3'),
            InlineKeyboardButton(text='4', callback_data='back')  # Кнопка "Назад" с callback
        ]
    ]
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Смотреть анкеты 💞'), KeyboardButton(text='Моя анкета 👤')],
        [KeyboardButton(text='Подписка 👑')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)


menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплата подписки', url='https://www.youtube.com/watch?v=HYi4a2eZL50')]
    ]
)


sex= ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Парень'), KeyboardButton(text='Девушка')]
        ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)


whoyowan= ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Парни'), KeyboardButton(text='Девушки')]
        ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)

react=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='❤️'), KeyboardButton(text='💌'), KeyboardButton(text='💔') , KeyboardButton(text='⬅️')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)
