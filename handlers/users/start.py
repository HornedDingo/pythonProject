from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp
from filters import IsPrivate

@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    kb_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Авторизоваться'),
                KeyboardButton(text='Зарегистрироваться')
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(f'Добро пожаловать в чат-бот для голосования. \n\nВыберите один из предложенных ниже вариантов действий.', reply_markup=kb_menu)

@dp.message_handler(IsPrivate(), text='Вернуться в главное меню')
async def command_start(message: types.Message):
    kb_menu2 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Авторизоваться'),
                KeyboardButton(text='Зарегистрироваться')
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(f'Добро пожаловать в чат-бот для голосования. \n\nВыберите один из предложенных ниже вариантов действий.',reply_markup=kb_menu2)