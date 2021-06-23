import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from emoji import emojize

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


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, from_user=None):
    button_tariffs = types.KeyboardButton(
                text='Тарифы 💸', call_data='tariffs'
            )
    button_my_entry = types.KeyboardButton(
                text='Моя запись 🔖', call_data='my_entry'
            )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(button_tariffs, button_my_entry)
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
        #db.subscribe(values) проверка на подписку через БД
    else:
        name = message.from_user.first_name
        values.append(str(message.from_user.first_name))
        values.append(message.from_user.last_name)
        values.append(message.from_user.username)
        #db.subscribe(values) проверка на подписку через БД
    reply = (
        f'Привет, {name} 👋 \nДобро пожаловать в kisihisi-bot\n'
    )

    reply2 = (
        'Чтобы записаться на прием выбери услугу и дату записи'
    )
    await message.answer(reply, reply_markup=keyboard)
    await message.answer(reply2, reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'services')
async def process_callback_services(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'services')


@dp.callback_query_handler(lambda c: c.data == 'date')
async def process_callback_date(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберите дату')
    

@dp.message_handler(commands=['help'])
async def help_text(message: types.Message):
    reply = (
        "Помощь по боту"
    )
    await message.answer(reply)


async def send_category_pages(message: types.Message, page):
    categories = db.get_categories() #нужно реализовать
    pages = 1
    if len(categories) % 10 == 0:
        pages = len(categories)//10
    else:
        pages = len(categories)//10 + 1
    paginator = InlineKeyboardPaginator(
        pages,
        current_page=page,
        data_pattern='category#{page}',
    )
    start_f = page * 10 - 10
    stop_f = page * 10
    cd = 'category#'
    # cd - callback data type
    
    if len(categories) < stop_f:
        stop_f = len(categories)

    for i in range(start_f, stop_f, 2):
        if stop_f != (i+1):
            paginator.add_before(
                InlineKeyboardButton(
                    categories[i][1],
                    callback_data=cd+str(categories[i][0])),
                InlineKeyboardButton(
                    categories[i+1][i],
                    callback_data=cd+str(categories[i+1][0])))
        else:




if __name__ == '__main__':
    executor.start_polling(dp)
