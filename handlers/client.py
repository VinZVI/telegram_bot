from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client, kb_dc
from aiogram.dispatcher.filters import Text

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# from aiogram.types import ReplyKeyboardRemove # класс удаляет клавиатуру
# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет!\
\nНапиши "Считать" для подсчета разности дат.',reply_markup=InlineKeyboardMarkup().\
                               add(InlineKeyboardButton('Считать', callback_data='Считать')))
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Date_countBot")

# @dp.callback_query_handler(text='Считать')
async def count_call (callback : types.Message):
    await callback.message.answer('Считать')

    await callback.answer()
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands='start')
    #dp.register_callback_query_handler(count_call, text='Считать')
    # dp.register_message_handler(commands_start, Text(equals='привет', ignore_case=True))