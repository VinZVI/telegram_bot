from re import fullmatch

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext  # хендлеры машины состояний
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.deep_linking import get_startgroup_link

from create_bot import bot
from function import Poll

polling_database = {}  # здесь хранится информация о опросах
polling_owners = {}  # здесь хранятся пары "id опроса <—> id её создателя"


class FSMclient(StatesGroup):
    poll_1 = State()  # состояние бота
    poll_2 = State()


# from aiogram.types import ReplyKeyboardRemove # класс удаляет клавиатуру
# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await bot.send_message(message.from_user.id, 'Привет!\
\nНапиши "Опрос", если нужно опросить всех членов группы.\
\nНапиши "Довести", если нужно довести информацию.\
\nНапиши "Считать" для подсчета разности дат.\
\n', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True). \
                               add(
            KeyboardButton('Опрос'), \
            KeyboardButton('Довести'), \
            KeyboardButton('Считать')))

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
            msg = await bot.send_poll(chat_id=message.chat.id, question='Жив, здоров?', is_anonymous=False,
                                      options=["ОК", "Не ОК"], type="regular", open_period=3600)
            # Сохраняем себе опрос в память
            polling_database[words[1]].append(Poll(
                poll_id_cl=msg.poll.id,
                question=msg.poll.question,
                options=[o.text for o in message.poll.options],
                chat_id=msg.chat.id,  # ... а также сохраняем chat_id ...
                message_id=msg.message_id)  # ... и message_id для последующего закрытия опроса.
            )
            # сохраняем опрос - викторина
            polling_owners[msg.poll.id] = str(words[1])


# Начало диалога Опроса
# @dp.message_handler(commands='Опрос', state=None)
async def cmd_start_poll(message: types.Message):
    await FSMclient.poll_1.set()
    poll_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    poll_kb.add(KeyboardButton(text="Отмена"))
    await message.reply('Введие сколько человек хотите опросить в группе.\n\
Если хотите начать заново введите "Отмена"', reply_markup=poll_kb)


# ловим первую дату
# @dp.message_handler(content_types=['poll_1'], state=FSMadmin.poll_1)
async def cmd_poll(message: types.Message, state: FSMContext):
    if not fullmatch(r"\b\d{1,2}\b", message.text):
        await message.reply('Пожалуйста, введие количестово людей целым числом не более 2х знаков')
        return
    # Если юзер раньше не присылал запросы, выделяем под него запись
    if not polling_database.get(str(message.from_user.id)):
        polling_database[str(message.from_user.id)] = []
    # добавляем в эту запись количество людей для опроса
    # polling_database[str(message.from_user.id)].append(Poll(count_pl_gr=int(message.text)))
    poll_keyboard = InlineKeyboardMarkup()
    poll_keyboard.add(InlineKeyboardButton(text="Создать опрос",
                                           url=await get_startgroup_link(str(message.from_user.id))))
    await message.reply("Нажмите на кнопку ниже и создайте опрос!", reply_markup=poll_keyboard)
    await state.finish()


# @dp.callback_query_handler(text='Довести')
async def count_call(callback: types.Message):
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
    dp.register_message_handler(cmd_start_poll, Text(equals='опрос', ignore_case=True), state=None)
    dp.register_message_handler(cmd_poll, state=FSMclient.poll_1)
    dp.register_callback_query_handler(count_call, text='Довести')
    # dp.register_message_handler(commands_start, Text(equals='привет', ignore_case=True))
