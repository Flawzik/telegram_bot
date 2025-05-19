from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Смотреть анкеты 💞'),KeyboardButton(text='Моя анкета 👤')],
        [KeyboardButton(text='Подписка 👑')]
],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню")

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оплата подписки',url='https://www.youtube.com/watch?v=HYi4a2eZL50')]
    ])

shalavi=['Shluha_1','shluha_2']

async def inline_shalavi():
    keyboard = InlineKeyboardBuilder()
    for shalavi in shalavi:
        keyboard.add(InlineKeyboardButton(text=shalavi))
    return keyboard.adjust(2).as_markup    

prof = ReplyKeyboardMarkup(keyboard_prof=[
        [KeyboardButton(text='1'),KeyboardButton(text='2'),[KeyboardButton(text='3')],[KeyboardButton(text='4')]]
],
    resize_keyboard_prof=True)
