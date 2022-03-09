from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

b1 = KeyboardButton('/Start')
b2 = KeyboardButton('/Help')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True) # , one_time_keyboard=True) # скрывает клавиатуру

kb_client.row(b1,b2)
