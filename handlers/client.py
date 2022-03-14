from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client, kb_dc
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# from aiogram.types import ReplyKeyboardRemove # класс удаляет клавиатуру
# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет!\
\nНапиши "Опрос", если нужно опросить всех членов группы.\
\nНапиши "Довести", если нужно довести информацию.\
\nНапиши "Считать" для подсчета разности дат.\
\n',reply_markup=InlineKeyboardMarkup().\
add(InlineKeyboardButton('Опрос', callback_data='Опрос'),\
InlineKeyboardButton('Довести', callback_data='Довести'),\
InlineKeyboardButton('Считать', callback_data='Считать')))
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Date_countBot")

# @dp.callback_query_handler(text='Считать')
async def count_call (callback : types.Message):
    await callback.answer('Тут будут другие функции')
    await callback.answer()

# Хэндлер на текстовое сообщение с текстом “Отмена”
# @dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands='start')
    dp.register_message_handler(action_cancel, commands='отмена')
    dp.register_message_handler(action_cancel, Text(equals='отмена', ignore_case=True))
    #dp.register_callback_query_handler(count_call, text=['Довести','Опрос'])
    # dp.register_message_handler(commands_start, Text(equals='привет', ignore_case=True))