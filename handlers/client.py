from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client
# from aiogram.types import ReplyKeyboardRemove # класс удаляет клавиатуру
# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет!\nНапиши "Считать" для подсчета разности дат.',\
        reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Date_countBot")

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
