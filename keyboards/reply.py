from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
# b1 = KeyboardButton(text='Авторизоваться')
# # b2 = KeyboardButton(text='Зарегистрироваться')
# kb_menu.add(b1)

kb_menu = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text='Авторизоваться', callback_data='start')
kb_menu.add(b1)

kb_main_btn = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text='Показать результаты', callback_data='show_old_q')
b2 = InlineKeyboardButton(text='Пройти новый опрос', callback_data='show_new_q')
kb_main_btn.add(b1).add(b2)

kb_menu3 = ReplyKeyboardMarkup(resize_keyboard=True)
b5 = KeyboardButton(text='Вернуться в меню')
kb_menu3.add(b5)

kb_menu4 = ReplyKeyboardMarkup(resize_keyboard=True)
b6 = KeyboardButton(text='Вернуться в главное меню')
kb_menu4.add(b6)

kb_poll_btn = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text='Следующий вопрос', callback_data='next_question')
b2 = InlineKeyboardButton(text='Отменить', callback_data='stop_poll')
kb_poll_btn.add(b1).add(b2)

kb_close_results = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text='Отменить', callback_data='close_results')
kb_close_results.add(b1)

kb_new_poll = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text='Продолжить', callback_data='continue_poll')
b2 = InlineKeyboardButton(text='Отменить', callback_data='close_poll')
kb_new_poll.add(b1).add(b2)

kb_go_back = InlineKeyboardMarkup()
b0 = InlineKeyboardButton(text='Вернуться в меню', callback_data='go_back')
kb_go_back.add(b0)
