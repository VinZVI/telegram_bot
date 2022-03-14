from typing import List

class Poll:
    type: str = "regular"

    def __init__(self, poll_id, question, options, owner_id):
        # Используем подсказки типов, чтобы было проще ориентироваться.
        self.poll_id: str = poll_id   # ID опроса. Изменится после отправки от имени бота
        self.question: str = question  # Текст вопроса
        self.options: List[str] = [*options] # "Распакованное" содержимое массива m_options в массив options
        self.owner: int = owner_id  # Владелец опроса
        self.winners: List[int] = []  # Список победителей
        self.chat_id: int = 0  # Чат, в котором опубликована опрос
        self.message_id: int = 0  # Сообщение с опросом (для закрытия)