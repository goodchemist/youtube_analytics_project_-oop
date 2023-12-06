import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется по id канала. Дальше все данные подтягиваются по API."""
        self.__channel_id = channel_id

        request = self.get_info_channel()

        self.title = request['items'][0]['snippet']['title']
        self.video_count = request['items'][0]['statistics']['videoCount']
        self.description = request['items'][0]['snippet']['description']
        self.view_count = request['items'][0]['statistics']['viewCount']
        self.subscriber_count = request['items'][0]['statistics']['subscriberCount']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id

    def get_info_channel(self):
        """
        Метод, возвращающий информацию о канале
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
        Класс-метод, возвращающий объект для работы с YouTube API
        :return: googleapiclient.discovery.Resource object
        """
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
