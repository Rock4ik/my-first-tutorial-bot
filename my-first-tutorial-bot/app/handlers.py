from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb

router = Router()

class Registration(StatesGroup):
    waiting_for_name = State()

user_names = {}

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!', reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')


@router.message(F.text == 'Как дела?')
async def how_are_you(message: Message):
    await message.answer('Все нормально :D')


@router.message(F.text == 'Покажи котиков')
async def get_photo(message: Message):
    await message.answer_photo(photo='https://s1.bloknot-voronezh.ru/thumb/850x0xcut/upload/iblock/509/0d1587dc21_7605080_8213488.jpg',
                               caption='Держи :3')
    
@router.message(F.text == 'Как настроение?')
async def how(message: Message):
    await message.answer('Сойдёт')

@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        'Привет', 
        reply_markup=kb.cataloganswer  # ← БЕЗ скобок!
    )

@router.message(Command('register'))
async def start_registration(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    if user_id in user_names:
        await message.answer("Ты уже зарегистрирован!")
        return
    
    await state.set_state(Registration.waiting_for_name)
    await message.answer("Как тебя зовут?")

@router.message(Registration.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()
    
    # Сохраняем ТОЛЬКО имя
    user_names[user_id] = name
    
    await state.clear()
    await message.answer(f"Приятно познакомиться, {name}! 😊")

@router.message(Command('profile'))
async def show_profile(message: Message):
    user_id = message.from_user.id
    
    if user_id in user_names:
        await message.answer(f"Твое имя: {user_names[user_id]}")
    else:
        await message.answer("Используй /register чтобы представиться")
