from function import Poll
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
# from create_bot import bot



# @dp.callback_query_handler(text='Опрос')
async def cmd_poll(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Создать опрос",
                                           request_poll=types.KeyboardButtonPollType(type=types.PollType.REGULAR)))
    poll_keyboard.add(types.KeyboardButton(text="Отмена"))
    await message.message.answer("Нажмите на кнопку ниже и создайте опрос!", reply_markup=poll_keyboard)
    await message.answer()

polling_database = {}  # здесь хранится информация о опросах
polling_owners = {}  # здесь хранятся пары "id опроса <—> id её создателя"

# @dp.message_handler(content_types=["poll"])
async def msg_with_poll(message: types.Message):
    # Если юзер раньше не присылал запросы, выделяем под него запись
    if not polling_database.get(str(message.from_user.id)):
        polling_database[str(message.from_user.id)] = []

    # Если юзер решил вручную отправить не викторину, а опрос, откажем ему.
    if message.poll.type != "regular":
        await message.reply("Извините, я принимаю только опросы (poll)!")
        return

    # Сохраняем себе викторину в память
    polling_database[str(message.from_user.id)].append(Poll(
        poll_id=message.poll.id,
        question=message.poll.question,
        options=[o.text for o in message.poll.options],
        owner_id=message.from_user.id)
    )
    # Сохраняем информацию о её владельце для быстрого поиска в дальнейшем
    polling_owners[message.poll.id] = str(message.from_user.id)
    print(message.poll.question, [o.text for o in message.poll.options])
    await message.reply(
        f"Опрос сохранен. Общее число сохранённых опросов: {len(polling_database[str(message.from_user.id)])}")

def register_handlers_polling(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_poll, text='Опрос')
    dp.register_message_handler(msg_with_poll, content_types=["poll"])
    # dp.register_message_handler(commands_start, Text(equals='привет', ignore_case=True))