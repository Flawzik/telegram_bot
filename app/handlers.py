from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import app.keyboards as kb
#from app.keyboards import prof

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply('HI', reply_markup=kb.main)

@router.message(F.text == 'Смотреть анкеты 💞')    
async def roum_prof(message: Message):
    await message.answer('Фото')

@router.message(F.text == 'Моя анкета 👤')    
async def my_prof(message: Message):
    await message.answer_photo(
        photo='AgACAgIAAxkBAAMQaCek7qN0uILsymUKoKFxyIveLuUAAp_zMRuxl0BJGOkPF0Xy9HEBAAMCAAN5AAM2BA',
        caption=f'Имя: {message.from_user.first_name}',
        reply_markup=kb.prof  # Исправлено название клавиатуры
    )
    lines = [
        '1. Смотреть анкеты.',
        '2. Заполнить анкету заново.',
        '3. Изменить фото/видео.',
        '4. Назад'
    ]
    await message.answer("\n".join(lines))

@router.message(F.text == 'Подписка 👑')    
async def pay_subscription(message: Message):
    await message.answer('Подписка', reply_markup=kb.menu)



                        

'''
@router.message(Command('get_photo'))    
async def get_photo(message:Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMQaCek7qN0uILsymUKoKFxyIveLuUAAp_zMRuxl0BJGOkPF0Xy9HEBAAMCAAN5AAM2BA',caption=message.from_user.first_name)
'''










'''
@router.message(Command())
async def cmd_settings(message:Message):
    await message.reply('Меню',reply_markup=kb.settings)   

async def show_inline_menu(message: types.Message):
    # Создаем inline-клавиатуру
    inline_builder = InlineKeyboardBuilder()
    inline_builder.button(text="Опция 1", callback_data="option1")
    inline_builder.button(text="Опция 2", callback_data="option2")
    inline_builder.button(text="Ссылка", url="https://example.com")
    inline_builder.adjust(2, 1)

    await message.answer(
        "Выберите опцию:",
        reply_markup=inline_builder.as_markup()
'''
