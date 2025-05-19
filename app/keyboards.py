from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

prof = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='1'), KeyboardButton(text='2')],
        [KeyboardButton(text='3'), KeyboardButton(text='4')]
    ],
    resize_keyboard=True
)

# Основная клавиатура
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Смотреть анкеты 💞'), KeyboardButton(text='Моя анкета 👤')],
        [KeyboardButton(text='Подписка 👑')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)

# Клавиатура для подписки
menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплата подписки', url='https://www.youtube.com/watch?v=HYi4a2eZL50')]
    ]
)

# Клавиатура для профиля (исправлено название и параметры)

'''     
shalavi=['Shluha_1','shluha_2']

async def inline_shalavi():
    keyboard = InlineKeyboardBuilder()
    for shalavi in shalavi:
        keyboard.add(InlineKeyboardButton(text=shalavi))
    return keyboard.adjust(2).as_markup    
  '''
