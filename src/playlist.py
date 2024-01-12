import datetime
import os
import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class PlayList:

    def __init__(self, playlist_id: str) -> None:

        """
        Экземпляр инициализируется по id плейлиста. Дальше все данные подтягиваются по API.

        :param playlist_id: id плейлиста
        """

        self.__playlist_id = playlist_id  # id плейлиста

        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'  # ссылкa на плейлист

        request_by_id = self.get_info_by_id()

        self.title = request_by_id["items"][0]["snippet"]["title"]  # название плейлиста

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API.

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

    def get_video_response(self, video_ids):
        """
        Метод, возвращающий информацию о видео из плейлиста по их id.

        :param video_ids: список всех id видео из плейлиста
        :return: словарь с информацией о видео из плейлиста по их id
        """
        youtube = self.get_service()
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        return video_response

    def get_info_about_playlist_videos(self):
        """
        Метод, возвращающий информацию об видео из плейлиста.

        :return: словарь с информацией об видео из плейлиста
        """
        youtube = self.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        return playlist_videos

    @staticmethod
    def get_video_ids(playlist_videos) -> list:
        """
        Метод, возвращающий список всех id видео из плейлиста.

        :param playlist_videos: словарь с информацией об видео из плейлиста
        :return: список всех id видео из плейлиста
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @property
    def total_duration(self) -> datetime.timedelta:
        """
        Возвращает суммарную длительность плейлиста.

        :return: объект класса datetime.timedelta
        """

        playlist_videos = self.get_info_about_playlist_videos()

        video_ids = self.get_video_ids(playlist_videos)

        video_response = self.get_video_response(video_ids)

        total_duration_ = datetime.timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)

            # Get datetime.timedelta object
            hours, minutes, seconds = str(duration).split(':')
            duration_timedelta = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

            # Calculate the total time
            total_duration_ += duration_timedelta

        return total_duration_

    def show_best_video(self) -> str:
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков).

        :return: ссылка на самое популярное видео
        """
        playlist_videos = self.get_info_about_playlist_videos()

        video_ids = self.get_video_ids(playlist_videos)

        video_response = self.get_video_response(video_ids)

        # Get dictionary with info about likes count for every video
        all_video = {}

        for id_, video in zip(video_ids, video_response['items']):
            like_count = video['statistics']['likeCount']
            all_video[id_] = like_count

        best_video = max(all_video, key=all_video.get)

        return f'https://youtu.be/{best_video}'
