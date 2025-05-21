from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType
from aiogram.types import ReplyKeyboardRemove
import app.keyboards as kb

router = Router()

class Reg(StatesGroup):
    name= State()
    age=State()
    sex=State()
    bio=State()
    city=State()
    whoyouwan=State()
    photo=State()

user_profiles= {}
'''    
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply('HI', reply_markup=kb.main)
''' 
@router.message(CommandStart())
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Давайте начнем регистрацию')
    await message.answer('👤 Введите ваше имя:')

@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.age)
    await message.reply('📅 Сколько вам лет?')

@router.message(Reg.age)
async def handle_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("❗ Пожалуйста, введите число!")
        return
    
    age = int(message.text)
    await state.update_data(age=age)
    await state.set_state(Reg.sex)
    await message.reply('👫 Выберите ваш пол:', reply_markup=kb.sex)

@router.message(Reg.sex)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await state.set_state(Reg.bio)
    await message.answer('💬 Расскажите о себе:',reply_markup=ReplyKeyboardRemove() )

@router.message(Reg.bio)
async def reg_four(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await state.set_state(Reg.city)
    await message.answer('🌍 Из какого вы города?')

@router.message(Reg.city)
async def reg_five(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Reg.whoyouwan)
    await message.reply(
        '❔ Кто вас интересуют?',
        reply_markup=kb.whoyowan  
    )

@router.message(Reg.whoyouwan)
async def reg_six(message: Message, state: FSMContext):
    await state.update_data(whoyouwan=message.text)
    await state.set_state(Reg.photo)
    
    await message.answer(
        "Пришлите фото/видео", 
        reply_markup=ReplyKeyboardRemove()  
    )

@router.message(Reg.photo, F.content_type.in_({ContentType.PHOTO, ContentType.VIDEO}))
async def handle_media(message: Message, state: FSMContext):
    media = message.photo[-1] if message.content_type == ContentType.PHOTO else message.video
    file_id = media.file_id
    
   
    data = await state.get_data()
    data['media'] = file_id
    
    
    user_profiles[message.from_user.id] = data  
    
    
    caption = (
        f"{data['name']}, {data['age']}, {data['city']}\n"
        f"{data['bio']}"
    )
    
    
    await message.answer_photo(
        photo=data['media'],
        caption=caption,
        reply_markup=kb.main
    )
    
    await state.clear()

@router.message(F.text == 'Моя анкета 👤')    
async def my_prof(message: Message):
    profile = user_profiles.get(message.from_user.id)
    caption = (
        f"{profile['name']}, {profile['age']}, {profile['city']}\n"
        f"{profile['bio']}"
    )
    
    
    await message.answer_photo(
        photo=profile['media'],
        caption=caption,
        reply_markup=kb.main
    )



'''    
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply('HI', reply_markup=kb.main)
'''
@router.message(F.text == 'Смотреть анкеты 💞')    
async def roum_prof(message: Message):
    await message.answer('Фото')

@router.message(F.text == 'Моя анкета 👤')    
async def my_prof(message: Message):
    await message.answer_photo(
        
        photo=data['media'],
        caption=caption,
        reply_markup=kb.main
    )
    
    await state.clear()

'''     
    lines = [
        '1. Смотреть анкеты.',
        '2. Заполнить анкету заново.',
        '3. Изменить фото/видео.',
        '4. Назад'
    ]
    await message.answer("\n".join(lines))


@router.callback_query(F.data == 'back')
async def back_handler(callback: CallbackQuery):
    await callback.message.edit_text(  
        text='Главное меню',
        reply_markup=None
    )
    await callback.message.answer(  
        'Вы вернулись в главное меню',
        reply_markup=kb.main
    )
    await callback.answer()  
'''

@router.message(F.text == 'Подписка 👑')    
async def pay_subscription(message: Message):
    await message.answer('Подписка', reply_markup=kb.menu)




