from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('working_mode')
b2 = KeyboardButton('job_places')
b3 = KeyboardButton('Share Contact', request_contact=True)
b4 = KeyboardButton('My Places', request_location=True)


kb_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_user.add(b1).add(b2).add(b3).add(b4)

