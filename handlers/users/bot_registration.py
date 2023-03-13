# import re
# import datetime
# from database.db import db
# from database.get import mysql6
# from database.create import mysql1, mysql2
# from aiogram import types
# from aiogram.types import ReplyKeyboardRemove
# from aiogram.dispatcher import FSMContext
# from keyboards.reply import kb_menu4
# from passlib.handlers.phpass import phpass
# from filters import IsPrivate
# from loader import dp
# from states import registrationpr
#
# cursor = db.cursor()
#
# cursor.execute("USE pollbase")
#
#
# @dp.message_handler(IsPrivate(), text='Зарегистрироваться')
# async def bot_register1(message: types.Message):
#     await message.answer(f'Здравствуйте, \n'
#                          f'для регистрации придумайте свой никнейм:', reply_markup=ReplyKeyboardRemove())
#     await registrationpr.user_nick.set()
#
#
# @dp.message_handler(IsPrivate(), state=registrationpr.user_nick)
# async def get_user_nick(message: types.Message, state: FSMContext):
#     answer = message.text
#     pattern = r"^.{2,15}$"
#     if re.match(pattern, answer):
#         await state.update_data(user_nick=message.text)
#         await state.update_data(user_display_name=message.text)
#         await message.answer(f'<b>{message.text}</b>, пожалуйста, напишите ваш номер телефона.')
#         await registrationpr.user_number.set()
#     else:
#         await message.answer(f'Введите корректный никнейм. \n\nОн должен умещаться в длину от 2 до 15 символов.')
#
#
# @dp.message_handler(IsPrivate(), state=registrationpr.user_number)
# async def get_phone(message: types.Message, state: FSMContext):
#     answer = message.text
#     phone_regex = re.compile("(\+7|8).*?(\d{2,3}).*?(\d{2,3}).*?(\d{2}).*?(\d{2})")
#     if phone_regex.match(answer):
#         await state.update_data(user_number=answer)
#         await message.answer(f'Ваш номер участка: ')
#         await registrationpr.user_area_number.set()
#     else:
#         await message.answer(f'Введите корректный номер телефона:')
#
#
# @dp.message_handler(IsPrivate(), state=registrationpr.user_area_number)
# async def get_user_area_number(message: types.Message, state: FSMContext):
#     answer = message.text
#     if answer.isnumeric():
#         if int(answer) < 150:
#             await state.update_data(user_area_number=answer)
#             await message.answer(f'Ваш адрес: ')
#             await registrationpr.user_address.set()
#
#         else:
#             await message.answer('Введите корректный номер участка:')
#     else:
#         await message.answer(f'Введите корректный номер участка:')
#
#
# @dp.message_handler(IsPrivate(), state=registrationpr.user_address)
# async def get_address(message: types.Message, state: FSMContext):
#     await state.update_data(user_address=message.text)
#     await message.answer(f'Ваша почта: ')
#     await registrationpr.user_email.set()
#
#
# @dp.message_handler(IsPrivate(), state=registrationpr.user_email)
# async def get_email(message: types.Message, state: FSMContext):
#     answer = message.text
#     email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
#     if email_regex.match(answer):
#         await state.update_data(user_email=answer)
#         await message.answer(f'Придумайте ваш будущий логин: ')
#         await registrationpr.user_lg.set()
#     else:
#         await message.answer(f'Введите корректный адрес электронной почты:')
#
#
# @dp.message_handler(IsPrivate(), state=registrationpr.user_lg)
# async def get_lg(message: types.Message, state: FSMContext):
#     answer = message.text
#     user_lg_regex = re.compile(r'^[a-zA-Z0-9]{3,14}$')
#     if user_lg_regex.match(answer):
#         await state.update_data(user_lg=message.text)
#         await message.answer(f'Придумайте ваш будущий пароль. \n\nОн должен : '
#                              f'\n1. Минимум одну цифру; '
#                              f'\n2. Одну заглавную букву и одну строчную букву; '
#                              f'\n3. Минимум один специальный символ; '
#                              f'\n4. Иметь длину от 6 до 20 символов.')
#         await registrationpr.user_pswd.set()
#     else:
#         await message.answer(f'Введите корректный логин. \n\nОн может содержать: '
#                              f'\n1. Латинские буквы; '
#                              f'\n2. Специальные символы; '
#                              f'\n3. Иметь длину от 6 до 15 символов.')
#
#
# @dp.message_handler(IsPrivate(), state=registrationpr.user_pswd)
# async def get_pswd(message: types.Message, state: FSMContext):
#     answer = message.text
#     pswd_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
#     if pswd_regex.match(answer):
#         await state.update_data(user_pswd=message.text)
#         await state.update_data(user_tg_id=message.from_user.id)
#         await state.update_data(user_url='telegram')
#         await state.update_data(user_regdate=datetime.datetime.now())
#         data = await state.get_data()
#         user_lg = data.get('user_lg')
#         user_pswd = data.get('user_pswd')
#         user_pswd3 = phpass.hash(user_pswd)
#         user_nick = data.get('user_nick')
#         user_email = data.get('user_email')
#         user_regdate = data.get('user_regdate')
#         user_url = data.get('user_url')
#         user_address = data.get('user_address')
#         user_area_number = data.get('user_area_number')
#         user_number = data.get('user_number')
#         user_tg_id = data.get('user_tg_id')
#         try:
#             val = (user_lg, user_pswd3, user_nick, user_email, user_url)
#             cursor.execute(mysql1, val)
#             db.commit()
#             cursor.execute(mysql6, (user_lg,))
#             userid2 = cursor.fetchone()
#             userid2 = int(''.join(map(str, userid2)))
#             val = (userid2, "phone", user_number)
#             cursor.execute(mysql2, val)
#             db.commit()
#             val = (userid2, "address", user_address)
#             cursor.execute(mysql2, val)
#             db.commit()
#             val = (userid2, "genplanno", user_area_number)
#             cursor.execute(mysql2, val)
#             db.commit()
#             val = (userid2, "telegramid", user_tg_id)
#             cursor.execute(mysql2, val)
#             db.commit()
#             val = (userid2, "auth_2", '0')
#             cursor.execute(mysql2, val)
#             db.commit()
#             db.close()
#             await message.answer(f'Регистрация завершена, ожидайте одобрения. \n'
#                                  f'Ваши данные: \n'
#                                  f'Никнейм:  {user_nick}\n'
#                                  f'Логин:  {user_lg}\n'
#                                  f'Пароль:  {user_pswd}\n'
#                                  f'Почта:  {user_email}\n'
#                                  f'Дата регистрации:  {user_regdate}\n'
#                                  f'Адрес:  {user_address}\n'
#                                  f'Номер участка:  {user_area_number}\n'
#                                  f'Телефон:  {user_number}\n', reply_markup=kb_menu4)
#         except Exception:
#             await message.answer(f'Вы уже зарегистрированы.', reply_markup=kb_menu4)
#         await state.finish()
#     else:
#         await message.answer(f'Введите корректный пароль. \n\nОн должен содержать: '
#                              f'\n1. Минимум одну цифру; '
#                              f'\n2. Одну заглавную букву и одну строчную букву; '
#                              f'\n3. Минимум один специальный символ; '
#                              f'\n4. Иметь длину от 6 до 20 символов.')
