import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('qbook.db')
    cur = base.cursor()
    if base:
        print("Data base connected OK")
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute("SELECT * FROM menu").fetchall():
        await message.bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}")
