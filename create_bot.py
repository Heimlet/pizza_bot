from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tokens import API_TOKEN


storage = MemoryStorage() # Самое простое хранилище. Использует оперативную память

bot = Bot(token=API_TOKEN) 
dp = Dispatcher(bot, storage=storage)
