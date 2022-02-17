from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove

from create_bot import bot, dp
from keyboards import kb_client
from data_base import sqlite_db

# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Welcome!', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/learning1999bot')


# @dp.message_handler(commands=['Schedule'])
async def pizza_schedule_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'Расписание:\nВс-Чт с 9:00 до 20:00\nПт-Сб с 10:00 до 23:00')

# @dp.message_handler(commands=['Location'])
async def pizza_location_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'ул. Колбасная, 15')

# @dp.message_handler(commands=['menu'])
async def pizza_menu_command(message : types.Message):
    await sqlite_db.sql_read(message)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_schedule_command, commands=['schedule'])
    dp.register_message_handler(pizza_location_command, commands=['location'])
    dp.register_message_handler(pizza_menu_command, commands=['menu'])