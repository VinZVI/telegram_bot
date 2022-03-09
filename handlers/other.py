from aiogram import types, Dispatcher
import json, string
from keyboards import kb_dc



#@dp.message_handler()# декоратор

async def filter_cenz(message : types.Message):
    if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('to_json\cenz.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()
    else:
        await message.reply('Нет такой команды, пожалуйста изпользуйте клавиатуру', reply_markup=kb_dc)
        await message.delete()


def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(filter_cenz)
