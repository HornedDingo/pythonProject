import re
import phonenumbers
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from passlib.handlers.phpass import phpass
from filters import IsPrivate
from loader import dp
from states import registration
import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rgaatrfla",
    port="3306",
    database="pollbase"
)


cursor = db.cursor()
cursor.execute("USE pollbase")

@dp.message_handler(IsPrivate(), text='Зарегистрироваться')
async def bot_register1(message: types.Message):
    await message.answer(f'Здравствуйте, \n'
                         f'для регистрации введите своё имя:')
    await registration.user_nick.set()

@dp.message_handler(IsPrivate(), Command('register'))
async def bot_register(message: types.Message):
    await message.answer(f'Здравствуйте, \n'
                         f'для регистрации введите своё имя:')
    await registration.user_nick.set()

@dp.message_handler(IsPrivate(), state=registration.user_nick)
async def get_user_nick(message: types.Message, state: FSMContext):
    await state.update_data(user_nick=message.text)
    await state.update_data(user_display_name=message.text)
    await message.answer(f'<b>{message.text}</b>, пожалуйста, напишите ваш номер телефона.')
    await registration.user_number.set()


@dp.message_handler(IsPrivate(), state=registration.user_number)
async def get_phone(message: types.Message, state: FSMContext):
    answer = message.text
    PHONE_REGEX = re.compile("(\+7|8).*?(\d{2,3}).*?(\d{2,3}).*?(\d{2}).*?(\d{2})")
    if PHONE_REGEX.match(answer):
        await state.update_data(user_number=answer)
        await message.answer(f'Ваш номер участка: ')
        await registration.user_area_number.set()
    else:
        await message.answer(f'Введите корректный номер телефона:')


@dp.message_handler(IsPrivate(), state=registration.user_area_number)
async def get_user_area_number(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isnumeric():
        if int(answer) <150:
            await state.update_data(user_area_number=answer)
            await message.answer(f'Ваш адрес: ')
            await registration.user_address.set()

        else:
            await message.answer('Введите корректный номер участка:')
    else:
        await message.answer(f'Введите корректный номер участка:')

@dp.message_handler(IsPrivate(), state=registration.user_address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(user_address=message.text)
    await message.answer(f'Ваша почта: ')
    await registration.user_email.set()


@dp.message_handler(IsPrivate(), state=registration.user_email)
async def get_email(message: types.Message, state: FSMContext):
    answer = message.text
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if EMAIL_REGEX.match(answer):
        await state.update_data(user_email=answer)
        await message.answer(f'Придумайте ваш будущий логин: '
                             f'\n\nОн должен иметь длину от 6 до 10 символов и НЕ содержать в себе спец. символы.')
        await registration.user_lg.set()
    else:
        await message.answer(f'Введите корректный адрес электронной почты:')


@dp.message_handler(IsPrivate(), state=registration.user_lg)
async def get_lg(message: types.Message, state: FSMContext):
    await state.update_data(user_lg=message.text)
    await message.answer(f'Придумайте ваш будущий пароль. \n\nОн должен : '
                             f'\n1. Минимум одну цифру; '
                             f'\n2. Одну заглавную букву и одну строчную букву; '
                             f'\n3. Минимум один специальный символ; '
                             f'\n4. Иметь длину от 6 до 20 символов.')
    await registration.user_pswd.set()


@dp.message_handler(IsPrivate(), state=registration.user_pswd)
async def get_pswd(message: types.Message, state: FSMContext):
    answer = message.text
    PSWD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
    if PSWD_REGEX.match(answer):
        await state.update_data(user_pswd=message.text)
        await state.update_data(user_tg_id=message.from_user.id)
        await state.update_data(user_url='telegram')
        await state.update_data(user_regdate=message.date)
        data = await state.get_data()
        user_lg = data.get('user_lg')
        user_pswd = data.get('user_pswd')
        user_pswd3 = phpass.hash(user_pswd)
        user_nick = data.get('user_nick')
        user_email = data.get('user_email')
        user_regdate = data.get('user_regdate')
        user_url = data.get('user_url')
        user_address = data.get('user_address')
        user_area_number = data.get('user_area_number')
        user_number = data.get('user_number')
        user_tg_id = data.get('user_tg_id')
        try:
            mysql = "INSERT INTO wp_users ( user_login, user_pass, user_nicename, user_email, user_url) VALUES (%s, %s, %s, %s, %s)"
            val = (user_lg, user_pswd3, user_nick, user_email, user_url)
            cursor.execute(mysql, val)
            db.commit()
            db.close()
            await message.answer(f'Регистрация завершена, ожидайте одобрения. \n'
                                 f'Ваши данные: \n'
                                 f'Никнейм:  {user_nick}\n'
                                 f'Логин:  {user_lg}\n'
                                 f'Пароль:  {user_pswd}\n'
                                 f'Почта:  {user_email}\n'
                                 f'Дата регистрации:  {user_regdate}\n'
                                 f'Адрес:  {user_address}\n'
                                 f'Номер участка:  {user_area_number}\n'
                                 f'Телефон:  {user_number}\n')

        except Exception as e:
            await message.answer(f'Вы уже зарегистрированы.')
        await state.finish()
    else:
        await message.answer(f'Введите корректный пароль. \n\nОн должен содержать: '
                             f'\n1. Минимум одну цифру; '
                             f'\n2. Одну заглавную букву и одну строчную букву; '
                             f'\n3. Минимум один специальный символ; '
                             f'\n4. Иметь длину от 6 до 20 символов.')
