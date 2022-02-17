import sqlite3 as sq

from create_bot import bot

def sql_start():
    """
    Инициализируем БД.


    Создаём БД, если её не существует, создаём таблицу `menu`, если её ...
    не существует и называем столбцы, обозначая типы.
    """
    global base, cur
    base = sq.connect('pizza_cool.db') # Подключаемсяс к бд, либо создаём, если её не существует.
    cur = base.cursor() # Курсор нужен, чтобы совершать операции в таблице (типа селектов и инсертов)
    if base:
        print('Database connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit() # Обязательно надо закрыть таблицу, сохранив действия


async def sql_add_command(state):
    """
    Добавляем в таблицу `menu` значения словаря.

    Конструкция вопросов вместо аргументов, и сразу же кортэж со значениями ВНЕ sql-запроса...
    ... предусмотрена для предотвращения sql-инъекций.
    """
    async with state.proxy() as data: 
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values())) # распаковываем словарь в таблицу, ...
        base.commit()                                                             # ... избегая sql-инъекций.

async def sql_read(message):
    """
    Отправляем данные из таблицы `menu`.

    Собираем данные из таблицы `menu` в массив, а затем отправляем их пользователю.
    """
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')

async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,)) # (data, ) должно быть кортежем, поэтому запятая.
    base.commit()