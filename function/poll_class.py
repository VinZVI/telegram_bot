from typing import List


class Poll:
    type: str = "regular"

    def __init__(self, poll_id, question, options, countPeoplGoup):
        # Используем подсказки типов, чтобы было проще ориентироваться.
        self.poll_id: str = poll_id  # ID опроса. Изменится после отправки от имени бота
        self.question: str = question  # Текст вопроса
        self.options: List[str] = [*options]  # "Распакованное" содержимое массива m_options в массив options
        self.owner: int = 0  # Владелец опроса
        self.countPeoplGoup: int = countPeoplGoup  # количество людей подлежащих опросу
        self.answer_ye: set(str) = set()  # Список ответивших положительно
        self.answer_no: set(str) = set()  # Список ответивших отрицательно
        self.chat_id: int = 0  # Чат, в котором опубликована опрос
        self.message_id: int = 0  # Сообщение с опросом (для закрытия)
