from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage() # запускаем место для хранени я ответов
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)