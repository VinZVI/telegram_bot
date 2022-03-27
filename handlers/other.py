import json
import string

from aiogram import types, Dispatcher


# @dp.message_handler()# декоратор

async def filter_cenz(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('to_json\cenz.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()

def register_handlers_other(dp : Dispatcher):
    # dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    # dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(filter_cenz)
