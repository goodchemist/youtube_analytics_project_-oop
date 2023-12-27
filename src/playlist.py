import datetime
import os
import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class PlayList:

    def __init__(self, playlist_id: str) -> None:

        self.__playlist_id = playlist_id  # id плейлиста

        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'  # ссылкa на плейлист

        request_by_id = self.get_info_by_id()

        self.title = request_by_id["items"][0]["snippet"]["title"]  # название плейлиста

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API
        :return: googleapiclient.discovery.Resource object
        """
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def get_info_by_id(self):
        """
        Метод, возвращающий информацию о плейлисте.
        :return: словарь с информацией о плейлисте
        """
        youtube = self.get_service()
        playlist = youtube.playlists().list(id=self.__playlist_id, part='snippet').execute()
        return playlist
