from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

b1 = KeyboardButton('/Start')
b2 = KeyboardButton('/Help')
b3 = KeyboardButton('/Считать')
b4 = KeyboardButton('/Результат')#, request_contact=True)
b5 = KeyboardButton('/Продолжить') #, request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True) # , one_time_keyboard=True) # скрывает клавиатуру

kb_client.row(b1,b2).add(b3).row(b4, b5)
