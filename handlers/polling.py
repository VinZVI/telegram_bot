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

ID = [467055923]

polling_database = {}  # здесь хранится информация о опросах
polling_owners = {}  # здесь хранятся пары "id опроса <—> id её создателя"


class FSMclient(StatesGroup):
    poll_1 = State()  # состояние бота
    poll_2 = State()


""" проверка на админа в группе """


# @dp.message_handler(commands='moderator', is_chat_admin=True)
async def commands_moderator(message: types.Message):
    global ID
    ID.append(message.from_user.id)
    print(ID)
    await bot.send_message(message.from_user.id, 'Что нужно хозяин?,\
\nНапиши "Опрос", если нужно опросить всех членов группы.\
\nНапиши "Довести", если нужно довести информацию.\
\n', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True). \
                           add(
        KeyboardButton('Опрос'), \
        KeyboardButton('Довести')))
    await message.delete()


# Начало диалога Опроса
# @dp.message_handler(commands='Опрос', state=None)
async def cmd_start_poll(message: types.Message):
    if message.from_user.id in ID:
        await FSMclient.poll_1.set()
        poll_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        poll_kb.add(KeyboardButton(text="Отмена"))
        await message.reply('Введие сколько человек хотите опросить в группе.\
\nЕсли хотите начать заново введите "Отмена"', reply_markup=poll_kb)


# ловим количество людей в группе которое нужно опросить
# @dp.message_handler(content_types=['poll_1'], state=FSMadmin.poll_1)
async def cmd_poll(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        if not fullmatch(r"\b\d{1,2}\b", message.text):
            await message.reply('Пожалуйста, введие количестово людей целым числом не более 2х знаков')
            return
        # Если юзер раньше не присылал запросы, выделяем под него запись
        if not polling_database.get(str(message.from_user.id)):
            polling_database[str(message.from_user.id)] = []
        # добавляем в эту запись количество людей для опроса
        polling_database[str(message.from_user.id)].append(Poll(
            poll_id=message.message_id,
            question='Жив, здоров?',
            options=["ОК", "Не ОК"],
            countPeoplGoup=int(message.text)))
        polling_owners[message.message_id] = str(message.from_user.id)
        # print(str(message.message_id))
        poll_keyboard = InlineKeyboardMarkup()
        poll_keyboard.add(InlineKeyboardButton(text="Создать опрос",
                                               url=await get_startgroup_link(str(message.message_id))))
        await message.reply("Нажмите на кнопку ниже и создайте опрос!", reply_markup=poll_keyboard)
        await state.finish()


# @dp.callback_query_handler(text='Довести')
async def count_call(message: types.Message):
    if message.from_user.id in ID:
        await message.reply('Тут будут другие функции')
        await message.delete()


# @dp.poll_answer_handler()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    """
    Это хендлер на новые ответы в опросах (Poll) и викторинах (Quiz)
    Реагирует на изменение голоса. В случае отзыва голоса тоже срабатывает!
    Чтобы не было путаницы:
    * quiz_answer - ответ на активную викторину
    * saved_quiz - викторина, находящаяся в нашем "хранилище" в памяти
    :param quiz_answer: объект PollAnswer с информацией о голосующем
    """
    poll_owner = polling_owners.get(poll_answer.poll_id)
    if not poll_owner:
        # logging.error(f"Не могу найти автора викторины с poll_answer.poll_id = {poll_answer.poll_id}")
        return
    for saved_poll in polling_database[poll_owner]:
        if saved_poll.poll_id == poll_answer.poll_id:
            # print(len(saved_poll.options))
            # сохраняем ответы пользователей
            for answer in range(0, len(saved_poll.options) - 1):
                if answer == poll_answer.option_ids[0]:
                    # Если OK, то добавляем в список положительных ответов
                    saved_poll.answer_ye.add(poll_answer.user.id)
                else:
                    # Если не OK, то добавляем в список отрицательных ответов
                    saved_poll.answer_no.add(poll_answer.user.id)
                # print(saved_poll.answer_ye, saved_poll.answer_no)
        # если все проголосовали, закрываем опрос.
        if len(saved_poll.answer_ye) + len(saved_poll.answer_no) == saved_poll.countPeoplGoup:
            # print(saved_poll.chat_id, saved_poll.message_id)
            print("опрос закрыт")
            await bot.stop_poll(saved_poll.chat_id[0], saved_poll.message_id)


# @dp.poll_handler(lambda active_quiz: active_quiz.is_closed is True)
async def just_poll_answer(active_poll: types.Poll):
    """
    Реагирует на закрытие опроса/викторины. Если убрать проверку на poll.is_closed == True,
    то этот хэндлер будет срабатывать при каждом взаимодействии с опросом/викториной, наравне
    с poll_answer_handler
    Чтобы не было путаницы:
    * active_quiz - викторина, в которой кто-то выбрал ответ
    * saved_quiz - викторина, находящаяся в нашем "хранилище" в памяти
    Этот хэндлер частично повторяет тот, что выше, в части, касающейся поиска нужного опроса в нашем "хранилище".
    :param active_quiz: объект Poll
    """
    poll_owner = polling_owners.get(active_poll.id)
    if not poll_owner:
        # logging.error(f"Не могу найти автора викторины с active_quiz.id = {active_quiz.id}")
        return
    for num, saved_poll in enumerate(polling_database[poll_owner]):
        if saved_poll.poll_id == active_poll.id:
            # Используем ID опрошеных, что бы показать кто что ответил.
            countAnswerYes = len(saved_poll.answer_ye)
            countAnswerNo = len(saved_poll.answer_no)
            if countAnswerNo == 0 and countAnswerYes == 0:
                await bot.send_message(saved_poll.chat_id[0], "Ответов не обнаружено!")
            else:
                await bot.send_message(saved_poll.chat_id[0], "Опрос закончен, всем спасибо!\n"
                                       + f"Всего было опрошено - {saved_poll.countPeoplGoup} человек")
                if countAnswerYes != 0:
                    congrats_text_ye = []
                    for user_id in saved_poll.answer_ye:
                        # print(saved_poll.chat_id[0], user, num)
                        chat_member_info = await bot.get_chat_member(saved_poll.chat_id[0], user_id)
                        congrats_text_ye.append(chat_member_info.user.get_mention(as_html=True))

                    await bot.send_message(saved_poll.chat_id[0], f"\nПроголосовало 'ОК' - {countAnswerYes} человек:\n"
                                           + "\n".join(congrats_text_ye), parse_mode="HTML")
                if countAnswerNo != 0:
                    congrats_text_no = []
                    for user_id in saved_poll.answer_no:
                        chat_member_info = await bot.get_chat_member(saved_poll.chat_id[0], user_id)
                        congrats_text_no.append(chat_member_info.user.get_mention(as_html=True))

                    await bot.send_message(saved_poll.chat_id[0], f"Проголосовало 'Не ОК' - {countAnswerYes} человек"
                                           + f"\nПозвоните начальнику:\n"
                                           + "\n".join(congrats_text_no), parse_mode="HTML")

            # Удаляем викторину из обоих наших "хранилищ"
            del polling_owners[active_poll.id]
            del polling_database[poll_owner][num]
        else:
            # logging.error(f"Не могу найти порос с saved_poll.poll_id == active_poll.id")
            return


def register_handlers_polling(dp: Dispatcher):
    dp.register_message_handler(commands_moderator, commands='moderator', is_chat_admin=True)
    dp.register_poll_answer_handler(handle_poll_answer)
    dp.register_poll_handler(just_poll_answer, lambda active_poll: active_poll.is_closed is True)
    dp.register_message_handler(cmd_start_poll, Text(equals='опрос', ignore_case=True), state=None)
    dp.register_message_handler(cmd_poll, state=FSMclient.poll_1)
    dp.register_message_handler(count_call, Text(equals='довести', ignore_case=True))
