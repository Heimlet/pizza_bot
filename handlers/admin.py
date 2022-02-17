from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb


ID = None

class FSMAdmin(StatesGroup):
    """
    Класс машины состояний.
    """
    photo = State()
    name = State()
    description = State()
    price = State()


# Получаем ID текущего модератора
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message : types.Message):
    """Получаем ID текущего модератора."""
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Хозяин, что надо???', reply_markup=admin_kb.button_case_admin)
    await message.delete()

# Выход из состояний
# @dp.message_handler(state="*", commands=['отмена', 'cancel'])
# @dp.message_handler(Text(equals=['отмена', 'cancel'], ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """Выход из состояний FSM."""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

# Начало диалога загрузки нового пункта меню в пиццерии
# @dp.message_handler(commands='Загрузить', state=None) # None т.к. это старт машины состояний
async def sm_start(message : types.Message):
    """
    Старт машины состояний.

    Запрашивает у пользователя отправку фото и ждёт её в хэндлере ...
    ... cостояния FSMAdmin.photo
    """
    if message.from_user.id == ID:
        await FSMAdmin.photo.set() # Благодаря этой команде бот понимает, что попадая в этот хэндлер ...
        await message.reply("Загрузите фото")             # пользователю надо запустить машину состояний

# Ловим первый ответ от пользователя
# @dp.message_hanler(content_types=['photo'], state=FSMAdmin.photo) # благодаря photo бот понимает, что в этот хэндлер перейдет SM после предыдщей функции
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Теперь введите название")

# Второй ответ пользователя
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите описание")

# Ловим третий ответ пользователя
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите цену")

# Ловим последний ответ и используемполученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await sqlite_db.sql_add_command(state)

        # async with state.proxy() as data:
        #     await message.reply(str(data))

        await state.finish() # С этой командой весь словарь очищается

@dp.callback_query_handler(Text(startswith='del ')) #or lambda x: x.data and x.data.statswith('del'))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)
    # await bot.answer_callback_query(callback_query.id, text...)    # второй вариант ответа

@dp.message_handler(commands=['Удалить', 'delete'])
async def delete_item(message: types.Message):
    """
    Отправляем админу фото, описание, цену товара, а также инлайн кнопку для удаления.
    """
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))




# Регистрируем хэндлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена', 'cancel'])
    dp.register_message_handler(cancel_handler, Text(equals=['отмена', 'cancel'], ignore_case=True), state="*")
    dp.register_message_handler(sm_start, commands=['Загрузить', 'upload'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_callback_query_handler(del_callback_run, Text(startswith='del '))
    dp.register_message_handler(delete_item, commands=['Удалить', 'delete'])