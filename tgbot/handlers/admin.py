from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State

from tgbot.keyboards.admin_button import button_case
from tgbot.models.sqlite_db import sql_add_command

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: Message):
    global ID
    ID = message.from_user.id
    await message.bot.send_message(message.from_user.id, "What need owner?", reply_markup=button_case)
    await message.delete()


async def start(message: Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply("Download photo")


async def load_photo(message: Message, state: FSMAdmin.photo):
    if message.from_user.id == ID:

        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Now you can enter a name")


async def load_name(message: Message, state: FSMContext):
    if message.from_user.id == ID:

        async with state.proxy() as data:
            data["name"] = message.text
        await FSMAdmin.next()
        await message.reply("Enter description")


async def load_description(message: Message, state: FSMContext):
    if message.from_user.id == ID:

        async with state.proxy() as data:
            data["description"] = message.text
        await FSMAdmin.next()
        return await message.reply("Now enter price")


async def load_price(message: Message, state: FSMContext):
    if message.from_user.id == ID:

        async with state.proxy() as data:
            data["price"] = float(message.text)
        # async with state.proxy() as data:
        #     await message.reply(str(data))
        await sql_add_command(state)
        await state.finish()



async def cancel_handler(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("OK")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(start, commands=["download"], state=None)
    dp.register_message_handler(load_photo, content_types=["photo"],  state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands="cancel")
    dp.register_message_handler(cancel_handler, Text(equals="cancel", ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
