from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler()# декоратор
async def echo_send(message : types.Message):
    await message.answer (message.text) #ждем своботное место в потоке команды
    # await message.reply(message.text)
    # await bot.send_message(message.from_user.id, message.text)



"""команда запуска бота"""
executor.start_polling(dp, skip_updates=True)
