from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove


b3 = KeyboardButton('/Считать')
b4 = KeyboardButton('/Результат')#, request_contact=True)
b5 = KeyboardButton('/Продолжить') #, request_location=True)

kb_dc = ReplyKeyboardMarkup(resize_keyboard=True) # , one_time_keyboard=True) # скрывает клавиатуру

kb_dc.add(b3).row(b4, b5)