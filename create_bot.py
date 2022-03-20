import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

storage = MemoryStorage()  # запускаем место для хранени я ответов
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)
