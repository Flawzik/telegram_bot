from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType
from aiogram.types import ReplyKeyboardRemove
from aiogram.exceptions import TelegramBadRequest  
from contextlib import closing
import logging
import sqlite3
import app.keyboards as kb
from app.database import (
    add_user,
    save_profile,
    get_profile,
    get_random_profile,
    add_like,
    check_match,
    add_match,
    get_likes_with_messages,
    DATABASE_NAME
)

router = Router()

class Reg(StatesGroup):
    name = State()
    age = State()
    sex = State()
    bio = State()
    city = State()
    whoyouwan = State()
    photo = State()

class SuperLikeState(StatesGroup):
    message = State()

@router.message(CommandStart())
async def reg_one(message: Message, state: FSMContext):
    add_user(message.from_user.id, 
           message.from_user.username,
           message.from_user.full_name)
    
    if get_profile(message.from_user.id):
        await message.answer("Главное меню:", reply_markup=kb.main)
        return
    
    await state.set_state(Reg.name)
    await message.answer("👋 Давайте создадим вашу анкету!\nВведите ваше имя:")

@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.age)
    await message.answer('📅 Сколько вам лет?')

@router.message(Reg.age)
async def handle_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Пожалуйста, введите число!")
        return
    
    age = int(message.text)
    await state.update_data(age=age)
    await state.set_state(Reg.sex)
    await message.reply('👫 Выберите ваш пол:', reply_markup=kb.sex)

@router.message(Reg.sex)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await state.set_state(Reg.bio)
    await message.answer('💬 Расскажите о себе:', reply_markup=ReplyKeyboardRemove())

@router.message(Reg.bio)
async def reg_four(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await state.set_state(Reg.city)
    await message.answer('🌍 Из какого вы города?')

@router.message(Reg.city)
async def reg_five(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Reg.whoyouwan)
    await message.answer('❔ Кто вас интересуют?', reply_markup=kb.whoyowan)

@router.message(Reg.whoyouwan)
async def handle_preferences(message: Message, state: FSMContext):
    valid = {'male', 'female', 'any'}
    
    
    user_input = message.text.lower()
    
   
    if user_input not in valid:
        await message.answer("🚫 Выберите вариант из клавиатуры!")
        return
    
    
    await state.update_data(preferences=user_input)
    await state.set_state(Reg.photo)
    await message.answer("📸 Теперь загрузите ваше фото/видео", reply_markup=ReplyKeyboardRemove())


@router.message(Reg.photo, F.content_type.in_({ContentType.PHOTO, ContentType.VIDEO}))
async def handle_media(message: Message, state: FSMContext):
    data = await state.get_data()
    
    if message.content_type == ContentType.PHOTO:
        media = message.photo[-1].file_id
        media_type = 'photo'
    else:
        media = message.video.file_id
        media_type = 'video'
    
    profile_data = {
        'name': data['name'],
        'age': data['age'],
        'gender': data['sex'],
        'city': data['city'],
        'bio': data['bio'],
        'preferences': data['whoyouwan'],
        'media': media,
        'media_type': media_type
    }
    
    save_profile(message.from_user.id, profile_data)
    await state.clear()
    
    if media_type == 'photo':
        await message.answer_photo(
            photo=media,
            caption=f"{data['name']}, {data['age']}, {data['city']}\n{data['bio']}",
            reply_markup=kb.main
        )
    else:
        await message.answer_video(
            video=media,
            caption=f"{data['name']}, {data['age']}, {data['city']}\n{data['bio']}",
            reply_markup=kb.main
        )
def save_profile(user_id, profile_data):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO profiles 
                  (user_id, name, age, gender, city, bio, media, media_type, preferences)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (user_id, 
                   profile_data['name'],
                   profile_data['age'],
                   profile_data['gender'],
                   profile_data['city'],
                   profile_data['bio'],
                   profile_data['media'],
                   profile_data['media_type'],
                   profile_data['preferences']))
        conn.commit()

@router.message(F.text == 'Моя анкета 👤')    
async def my_prof(message: Message):
    profile = get_profile(message.from_user.id)
    if profile:
        _, _, name, age, _, city, bio, media, media_type, _ = profile
        
        try:
            if media_type == 'photo':
                await message.answer_photo(
                    photo=media,
                    caption=f"{name}, {age}\n{city}\n\n{bio}",
                    reply_markup=kb.main
                )
            else:
                await message.answer_video(
                    video=media,
                    caption=f"{name}, {age}\n{city}\n{bio}",
                    reply_markup=kb.main
                )
        except TelegramBadRequest:
            await message.answer("❌ Медиафайл недоступен. Обновите анкету!")
    else:
        await message.answer("❌ Вы еще не создали анкету!")

@router.message(F.text == 'Смотреть анкеты 💞')    
async def roum_prof(message: Message):
    current_profile = get_profile(message.from_user.id)
    if not current_profile:
        await message.answer("❌ Сначала создайте анкету!")
        return

    
    *_, preferences = current_profile  

    
    profile = get_random_profile(
        current_user_id=message.from_user.id,
        current_preferences=preferences
    )

    if profile:
        *_, gender, city, bio, media, _ = profile
        await message.answer_photo(
            photo=media,
            caption=f"{gender} 👤\n{city}\n\n{bio}",
            reply_markup=kb.react
        )
    else:
        await message.answer("😔 Нет подходящих анкет")

@router.message(F.text == '💌')
async def start_superlike(message: Message, state: FSMContext):
    profile = get_random_profile(message.from_user.id)
    if profile:
        await state.update_data(target_id=profile[1])
        await state.set_state(SuperLikeState.message)
        await message.answer("💌 Напишите сообщение для этого лайка:", reply_markup=ReplyKeyboardRemove())

@router.message(SuperLikeState.message)
async def save_superlike(message: Message, state: FSMContext):
    data = await state.get_data()
    target_id = data['target_id']
    
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO likes (liker_id, target_id) VALUES (?, ?)', 
                 (message.from_user.id, target_id))
        like_id = c.lastrowid
        
        c.execute('INSERT INTO like_messages (like_id, message) VALUES (?, ?)',
                 (like_id, message.text))
        conn.commit()
    
    await message.answer("💌 Лайк с сообщением отправлен!", reply_markup=kb.main)
    await state.clear()
''' 
@router.message(F.text == 'Мои лайки 💌')
async def show_likes(message: Message):
    likes = get_likes_with_messages(message.from_user.id)
    if likes:
        for like in likes:
            _, name, message_text = like
            msg = f"❤️ Лайк от {name}"
            if message_text:
                msg += f"\n💌 Сообщение: {message_text}"
            await message.answer(msg)
    else:
        await message.answer("У вас пока нет лайков 😔")
'''
@router.message(F.text == 'Подписка 👑')    
async def pay_subscription(message: Message):
    await message.answer('Подписка', reply_markup=kb.menu)

@router.message(F.text == '⬅️')    
async def go_back(message: Message):
    await message.answer('Главное меню', reply_markup=kb.main)
