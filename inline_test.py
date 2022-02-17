from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tokens import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

answ = dict()

# Кнопка ссылка
urlkb = InlineKeyboardMarkup(row_width=2)
urlButton = InlineKeyboardButton(text='Ссылка', url='https://youtube.com')
urlButton2 = InlineKeyboardButton(text='Ссылка2', url='https://google.com')
x = [InlineKeyboardButton(text='Ссылка3', url='https://google.com'), InlineKeyboardButton(text='Ссылка4', url='https://google.com'),\
    InlineKeyboardButton(text='Ссылка5', url='https://google.com')]
urlkb.add(urlButton, urlButton2).row(*x).insert(InlineKeyboardButton(text='Ссылка6', url='https://google.com'))

@dp.message_handler(commands=['ссылки', 'links'])
async def url_command(message : types.Message):
    await message.answer('Ссылочки:', reply_markup=urlkb)


inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='like', callback_data='like_1'),\
                                            InlineKeyboardButton(text='dislike', callback_data='like_-1'))

@dp.message_handler(commands='test')
async def test_commands(message : types.Message):
    await message.answer('За видео про деплой бота', reply_markup=inkb)

@dp.callback_query_handler(Text(startswith='like_'))
async def www_call(callback_Example : types.CallbackQuery):
    """По ключу id записываем результат 1 или -1"""
    result = int(callback_Example.data.split('_')[1])
    if f'{callback_Example.from_user.id}' not in answ:
        answ[f'{callback_Example.from_user.id}'] = result
        await callback_Example.answer('Вы проголосовали')
    else:
        await callback_Example.answer('Вы уже проголосовали', show_alert=True)

    # await callbackExample.message.answer('Вы нажали inline-кнопку')
    # await callbackExample.answer('Вы нажали inline-кнопку')
    # await callbackExample.answer('Нажата inline-кнопка', show_alert=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)