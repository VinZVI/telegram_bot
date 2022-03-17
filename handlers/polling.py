import logging

from aiogram import types, Dispatcher

from create_bot import bot
from handlers.client import polling_database, polling_owners


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
        logging.error(f"Не могу найти автора викторины с poll_answer.poll_id = {poll_answer.poll_id}")
        return
    for saved_poll in polling_database[poll_owner]:
        if saved_poll.poll_id_cl == poll_answer.poll_id:
            # сохраняем ответы пользователей
            if saved_poll.options[0] == poll_answer.option_ids[0]:
                # Если OK, то добавляем в список положительных ответов
                saved_poll.answer_ye.add(poll_answer.user.id)
            else:
                # Если не OK, то добавляем в список отрицательных ответов
                saved_poll.answer_no.add(poll_answer.user.id)
                # По нашему условию, если есть двое правильно ответивших, закрываем викторину.
        if len(saved_poll.answer_ye) + len(saved_poll.answer_no) == 1:
            print("опрос закрыт")
            await bot.stop_poll(saved_poll.chat_id, saved_poll.message_id)


# @dp.poll_handler(lambda active_quiz: active_quiz.is_closed is True)
async def just_poll_answer(active_quiz: types.Poll):
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
    quiz_owner = quizzes_owners.get(active_quiz.id)
    if not quiz_owner:
        logging.error(f"Не могу найти автора викторины с active_quiz.id = {active_quiz.id}")
        return
    for num, saved_quiz in enumerate(quizzes_database[quiz_owner]):
        if saved_quiz.quiz_id == active_quiz.id:
            # Используем ID победителей, чтобы получить по ним имена игроков и поздравить.
            congrats_text = []
            for winner in saved_quiz.winners:
                chat_member_info = await bot.get_chat_member(saved_quiz.chat_id, winner)
                congrats_text.append(chat_member_info.user.get_mention(as_html=True))

            await bot.send_message(saved_quiz.chat_id, "Викторина закончена, всем спасибо! Вот наши победители:\n\n"
                                   + "\n".join(congrats_text), parse_mode="HTML")
            # Удаляем викторину из обоих наших "хранилищ"
            del quizzes_owners[active_quiz.id]
            del quizzes_database[quiz_owner][num]


def register_handlers_polling(dp: Dispatcher):
    dp.register_poll_answer_handler(handle_poll_answer)
    # dp.register_callback_query_handler(cmd_poll, text='Опрос')
# dp.register_message_handler(msg_with_poll, content_types=["poll"])
# dp.register_message_handler(commands_start, Text(equals='привет', ignore_case=True))"""
