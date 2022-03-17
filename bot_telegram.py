import logging

from aiogram.utils import executor

from create_bot import dp
from handlers import client, other, date_count_handlers, polling

logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)

async def on_startup(_):
    print('Бот вышел в онлайн')
    # sqlite_db.sql_start() # запускаем функцию базы данных


client.register_handlers_client(dp)
polling.register_handlers_polling(dp)
date_count_handlers.register_handlers_dc(dp)
other.register_handlers_other(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
