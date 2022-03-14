from aiogram.utils import executor
from create_bot import dp
from date_base import sqlite_db


async def on_startup(_):
    print('Бот вышел в онлайн')
    # sqlite_db.sql_start() # запускаем функцию базы данных


from handlers import client, polling, other, date_count_handlers

client.register_handlers_client(dp)
polling.register_handlers_polling(dp)
date_count_handlers.register_handlers_dc(dp)
other.register_handlers_other(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
