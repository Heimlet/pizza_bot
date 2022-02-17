from aiogram import executor

from create_bot import dp
from handlers import client, admin, other
from data_base import sqlite_db


async def on_startup(_):
    print('Bot ONLINE now')
    sqlite_db.sql_start()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

