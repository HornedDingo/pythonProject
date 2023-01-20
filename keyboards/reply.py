from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='Авторизоваться')
b2 = KeyboardButton(text='Зарегистрироваться')
kb_menu.add(b1).insert(b2)

kb_menu2 = ReplyKeyboardMarkup(resize_keyboard=True)
b3 = KeyboardButton(text='Авторизоваться')
b4 = KeyboardButton(text='Проверить статус регистрации')
kb_menu2.add(b3).insert(b4)

kb_menu3 = ReplyKeyboardMarkup(resize_keyboard=True)
b5 = KeyboardButton(text='Вернуться в меню')
kb_menu3.add(b5)

kb_menu4 = ReplyKeyboardMarkup(resize_keyboard=True)
b6 = KeyboardButton(text='Вернуться в главное меню')
kb_menu4.add(b6)
