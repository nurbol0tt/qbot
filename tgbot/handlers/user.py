from aiogram import Dispatcher, Bot
from aiogram.types import Message

from tgbot.keyboards.reply import kb_user
from tgbot.models.sqlite_db import sql_read

CHAT_ID = -813360773


async def user_start(message: Message):
    await message.reply("Hello, user!")


async def command_start(message: Message):
    try:
        await message.bot.send_message(message.from_user.id,
                                       'Привет Меня зовут Qbot, я буду твои помощником',
                                       reply_markup=kb_user)
    except:
        await message.reply("Напишите боту")


async def working_mode(message: Message):
    await message.bot.send_message(message.from_user.id, 'Пн-ПТ с 8:00 до 6:00')


async def job_places(message: Message):
    await message.bot.send_message(message.from_user.id, 'г.Бишкек ул.Ошская 46')


async def menu_command(message: Message):
    await sql_read(message)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start2"], state="*")
    dp.register_message_handler(command_start, commands=["start"], state="*")
    dp.register_message_handler(working_mode, commands=["working_mode"], state="*")
    dp.register_message_handler(job_places, commands=["job_places"], state="*")
    dp.register_message_handler(menu_command, commands=["menu"])
