from typing import List, Set

class Poll:
    type: str = "regular"

    def __init__(self, poll_id, question, options, owner_id):
        # Используем подсказки типов, чтобы было проще ориентироваться.
        self.poll_id_cl: str = poll_id  # ID опроса. Изменится после отправки от имени бота
        self.question: str = question  # Текст вопроса
        self.options: List[str] = [*options]  # "Распакованное" содержимое массива m_options в массив options
        self.owner: int = owner_id  # Владелец опроса
        self.count_pl_gr: int = 0  # количество людей подлежащих опросу
        self.answer_ye: Set[str] = {}  # Список ответивших положительно
        self.answer_no: Set[str] = {}  # Список ответивших отрицательно
        self.chat_id: int = 0  # Чат, в котором опубликована опрос
        self.message_id: int = 0  # Сообщение с опросом (для закрытия)
