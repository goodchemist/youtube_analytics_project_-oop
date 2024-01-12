import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется по id канала. Дальше все данные подтягиваются по API.

        :param channel_id: id канала
        """

        self.__channel_id = channel_id  # id канала

        request = self.get_info_channel()

        self.title = request['items'][0]['snippet']['title']  # название канала
        self.video_count = int(request['items'][0]['statistics']['videoCount'])  # количество видео
        self.description = request['items'][0]['snippet']['description']  # описание
        self.view_count = int(request['items'][0]['statistics']['viewCount'])  # количество просмотров
        self.subscriber_count = int(request['items'][0]['statistics']['subscriberCount'])  # количество подписчиков
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id  # ссылка на канал

    def __str__(self):
        """
        Возвращает информацию об объекте класса в удобном для пользователя виде.

        :return: f-строка с названием канала и url-ссылкой
        """
        return f'{self.title} ({self.url})'

    def __add__(self, other: 'Channel') -> int:
        """
        Складывает количество подписчиков в двух каналах.

        :param other: экзепляр класса Channel
        :return: общее количество подписчиков в двух каналах
        """
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """
        Вычитает количество подписчиков одного канала из другого.

        :param other: экзепляр класса Channel
        :return: разница в количестве подписчиков между первым и вторым каналами
        """
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        """
        Метод для операции сравнения "больше".

        :param other: экзепляр класса Channel
        :return: True или False
        """
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """
        Метод для операции сравнения "больше или равно" по числу подписчиков.

        :param other: экзепляр класса Channel
        :return: True или False
        """
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """
        Метод для операции сравнения "меньше" по числу подписчиков.

        :param other: экзепляр класса Channel
        :return: True или False
        """
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """
        Метод для операции сравнения "меньше или равно" по числу подписчиков.

        :param other: экзепляр класса Channel
        :return: True или False
        """
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        """
        Метод для операции сравнения "равно" по числу подписчиков.

        :param other: экзепляр класса Channel
        :return: True или False
        """
        return self.subscriber_count == other.subscriber_count

    def get_info_channel(self):
        """
        Метод, возвращающий информацию о канале.

        :return: словарь с информацией о канале
        """
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        channel = self.get_info_channel()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API.

        :return: googleapiclient.discovery.Resource object
        """
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, name_of_file) -> None:
        """
        Метод, сохраняющий в файл значения атрибутов экземпляра Channel.

        :param name_of_file: имя файла
        """

        json_dict = {
            "id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriberCount": self.subscriber_count,
            "videoCount": self.video_count,
            "viewCount": self.view_count
        }

        with open(name_of_file, 'w') as file:
            json.dump(json_dict, file)
