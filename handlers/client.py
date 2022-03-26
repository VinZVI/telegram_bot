from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from create_bot import bot
from handlers.polling import polling_database, polling_owners, ID


# from aiogram.types import ReplyKeyboardRemove # класс удаляет клавиатуру
# @dp.message_handler(commands=['start', 'help'])
async def commands_start_client(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        if message.from_user.id in ID:
            await message.reply('Что нужно хозяин?,\
\nНапиши "Опрос", если нужно опросить всех членов группы.\
\nНапиши "Довести", если нужно довести информацию.\
\n', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True). \
                                add(KeyboardButton('Опрос'), \
                                    KeyboardButton('Довести')))
        else:
            await message.reply('Привет!\
\nНапиши "Считать" для подсчета разности дат.\
\n', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True). \
                                add(KeyboardButton('Считать')))
        await message.delete()
    else:
        words = message.text.split()
        # Только команда /start без параметров. В этом случае отправляем в личку с ботом.
        if len(words) == 1:
            bot_info = await bot.get_me()  # Получаем информацию о нашем боте
            keyboard = types.InlineKeyboardMarkup()  # Создаём клавиатуру с URL-кнопкой для перехода в ЛС
            move_to_dm_button = types.InlineKeyboardButton(text="Перейти в ЛС",
                                                           url=f"t.me/{bot_info.username}?start=anything")
            keyboard.add(move_to_dm_button)
            await message.reply("Общение с ботом через ЛС, напишите ему:", reply_markup=keyboard)
        # Если у команды /start или /startgroup есть параметр, то это, скорее всего, парпметр Опроса - 'Poll'.
        # Проверяем и отправляем.
        else:
            poll_owner = polling_owners.get(int(words[1]))
            # print(poll_owner, polling_owners)
            if not poll_owner:
                await message.reply(
                    "Попробуйте создать новый опрос. /start")
                return
            for seved_poll in polling_database[str(poll_owner)]:
                # print(seved_poll.poll_id, words[1])
                if seved_poll.poll_id == int(words[1]):
                    msg = await bot.send_poll(chat_id=message.chat.id, question=seved_poll.question, is_anonymous=False,
                                              options=seved_poll.options, type="regular", open_period=360)
                    polling_owners[msg.poll.id] = poll_owner  # сохраняем опрос - викторина
                    del polling_owners[int(words[1])]  # удаляем старую запись
                    seved_poll.poll_id = msg.poll.id  # записываем id опроса в базу
                    seved_poll.chat_id = msg.chat.id,  # ... а также сохраняем chat_id ...
                    seved_poll.message_id = msg.message_id  # ... и message_id для последующего закрытия опроса.
                    # print(msg.chat.id, msg.message_id)
                # else:
                #     await message.reply(
                #         "Попробуйте создать новый опрос2. /start")
                #     return




# Хэндлер на текстовое сообщение с текстом “Отмена”
# @dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново.", \
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True). \
                         add(KeyboardButton('/start')))
    await message.delete()
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start_client, commands='start')
    dp.register_message_handler(action_cancel, commands='отмена')
    dp.register_message_handler(action_cancel, Text(equals='отмена', ignore_case=True))
