from aiogram import types, Dispatcher
import json, string
from keyboards import kb_dc
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext


#@dp.message_handler()# декоратор

async def filter_cenz(message : types.Message):
    if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('to_json\cenz.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()
    else:
        await message.reply('Нет такой команды, пожалуйста изпользуйте клавиатуру', reply_markup=kb_dc)
        await message.delete()

# вывод из состояний
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
# async def cancel_handler(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=types.ReplyKeyboardRemove())

def register_handlers_other(dp : Dispatcher):
    # dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    # dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(filter_cenz)
