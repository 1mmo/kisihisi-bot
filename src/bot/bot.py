import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from common import db

from keyboard.pagination_kb import InlineKeyboardPaginator


API_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(
        filename='bot.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S')

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.callback_query_handler(lambda c: c.data == 'back_to_services')
async def procces_callback_back_to_services(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await send_menu(callback_query.message)


@dp.callback_query_handler(lambda c: c.data == 'back_to_menu')
async def process_callback_back_to_menu(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await send_menu(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'procedures')
async def procces_callback_procedures(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await send_procedures_pages(callback_query.message, 1)
    

@dp.callback_query_handler(lambda c: c.data == 'complex')
async def procces_callback_complex(callback_query: types.CallbackQuery):
    await send_complex_pages(callback_query, 1)


@dp.callback_query_handler(lambda c: c.data == 'services')
async def procces_callback_services(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    inline_complex = InlineKeyboardButton('Комплексы', callback_data='complex')
    inline_procedures = InlineKeyboardButton('Процедуры', callback_data='procedures')
    inline_back = InlineKeyboardButton('Назад', callback_data = 'back_to_menu')
    inline_kb = InlineKeyboardMarkup().row(inline_procedures, inline_complex)
    inline_kb.add(inline_back)
    reply = (
            'ПРАЙС\nКоплексы\nДолговременная укладка         1200 руб\n+коррекция\n+окрашивание хной/краской'
    )
    await bot.send_message(callback_query.from_user.id, text=reply,  reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data == 'date')
async def process_callback_date(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберите дату')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, from_user=None):
    button_location = types.KeyboardButton(
                text='Локация 📍', call_data='location'
            )
    button_my_entry = types.KeyboardButton(
                text='Моя запись 🔖', call_data='my_entry'
            )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(button_location, button_my_entry)
    inline_button_services = InlineKeyboardButton('Услуги 🥰', callback_data='services')
    inline_button_date = InlineKeyboardButton('Дата 🗓', callback_data='date')
    inline_kb = InlineKeyboardMarkup().row(inline_button_services, inline_button_date)
    values = []
    if from_user:
        name = from_user.first_name
        values.append(str(from_user.id))
        values.append(from_user.first_name)
        values.append(from_user.last_name)
        values.append(from_user.username)
        db.subscribe(values)
    else:
        name = message.from_user.first_name
        values.append(str(message.from_user.id))
        values.append(message.from_user.first_name)
        values.append(message.from_user.last_name)
        values.append(message.from_user.username)
        db.subscribe(values)    
    reply = (
        f'Привет {name} 👋 \nДобро пожаловать в kisihisi-bot\n'
    )
    await message.answer(reply, reply_markup=keyboard)
    await send_menu(message)


@dp.message_handler(commands=['help'])
async def help_text(message: types.Message):
    reply = (
        "Помощь по боту"
    )
    await message.answer(reply)


@dp.message_handler()
async def message_parse(message: types.Message):
    if 'Локация' in message.text:
        inline_back = InlineKeyboardButton('Назад 👈', callback_data = 'back_to_menu')
        inline_kb = InlineKeyboardMarkup().add(inline_back)
        reply = 'Нижний Новгород, площадь Максима Горького, 4/2'
        await bot.send_location(message.from_user.id, 56.314576, 43.99056)
        await message.answer(text=reply, reply_markup=inline_kb)
    elif 'Моя запись' in message.text:
        reply = 'My entry'
        await message.answer(reply)
    else:
        reply = ('Непонятное сообщение, попробуй снова')
        await message.answer(reply)


async def send_procedures_pages(message: types.Message, page):
    procedures = db.get_procedures()
    pages = 1
    if len(procedures) % 10 == 0:
        pages = len(procedures)//10
    else:
        pages = len(procedures)//10 + 1
    paginator = InlineKeyboardPaginator(
        pages,
        current_page=page,
        data_pattern='procedures#{page}',
    )
    start_f = page * 10 - 10
    stop_f = page * 10
    cd = 'procedures_value#'
    # cd - callback data type

    if len(procedures) < stop_f:
        stop_f = len(procedures)

    for i in range(start_f, stop_f, 2):
        if stop_f != (i + 1):
            paginator.add_before(
                InlineKeyboardButton(
                    procedures[i][1],
                    callback_data=cd+str(procedures[i][0])))
            paginator.add_before(
                InlineKeyboardButton(
                    procedures[i+1][1],
                    callback_data=cd+str(procedures[i+1][0])))
        else:
            paginator.add_before(
                    InlineKeyboardButton(
                        procedures[i][1],
                        callback_data=cd+str(procedures[i][0])))

    paginator.add_after(InlineKeyboardButton('Назад 👈', callback_data='back_to_services'))

    await bot.send_message(
            message.chat.id,
            text=f'Услуги {page}',
            reply_markup=paginator.markup,
    )


async def send_menu(message: types.Message):
    inline_button_services = InlineKeyboardButton('Услуги 🥰', callback_data='services')
    inline_button_date = InlineKeyboardButton('Дата 🗓', callback_data='date')
    inline_kb = InlineKeyboardMarkup().row(inline_button_services, inline_button_date)
    reply = (
        'Чтобы записаться на прием выбери услугу и дату записи'
    )
    await message.answer(reply, reply_markup=inline_kb)


if __name__ == '__main__':
    executor.start_polling(dp)
