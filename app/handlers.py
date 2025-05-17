from aiogram import F,Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import app.keyboards as kb


router=Router()

@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.reply('HI',reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message:Message):
    await message.answer("/help")

#@router.message(Command ('profile'))
#async def profile(message:Message):
#    await message.reply(photo='AgACAgIAAxkBAAMQaCek7qN0uILsymUKoKFxyIveLuUAAp_zMRuxl0BJGOkPF0Xy9HEBAAMCAAN5AAM2BA',caption=f'Имя:{message.from_user.first_name}')

@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.reply(message.from_user.id,' ',message.from_user.first_name)


#@router.message(F.text =='Моя анкета')
#async def My_profile(message:Message):
#    await message.answer(photo='AgACAgIAAxkBAAMQaCek7qN0uILsymUKoKFxyIveLuUAAp_zMRuxl0BJGOkPF0Xy9HEBAAMCAAN5AAM2BA',
#                         caption=f'Имя:{message.from_user.first_name}')

@router.message(Command('get_photo'))    
async def get_photo(message:Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMQaCek7qN0uILsymUKoKFxyIveLuUAAp_zMRuxl0BJGOkPF0Xy9HEBAAMCAAN5AAM2BA',caption=message.from_user.first_name)

@router.message(F.photo)    
async def get_photo(message:Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')
