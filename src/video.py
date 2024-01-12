import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Video:

    def __init__(self, video_id: str) -> None:
        """
        Экземпляр инициализируется по id видео. Дальше все данные подтягиваются по API.

        :param video_id: id видео
        """
        self.video_id = video_id  # id видео

        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()

        try:
            self.video_title: str = video_response['items'][0]['snippet']['title']  # название видео
            self.view_count: int = int(video_response['items'][0]['statistics']['viewCount'])  # количество просмотров
            self.like_count: int = int(video_response['items'][0]['statistics']['likeCount'])  # количество лайков
            self.comment_count: int = int(video_response['items'][0]['statistics']['commentCount'])  # количество комм-й

        except IndexError:
            self.video_title = None  # название видео
            self.view_count = None  # количество просмотров
            self.like_count = None  # количество лайков
            self.comment_count = None  # количество комментарий

    def __str__(self) -> str:
        """
        Возвращает информацию об объекте класса в удобном для пользователя виде.

        :return: название видео
        """
        return self.video_title


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """
        Экземпляр инициализируется по id видео и id плейлиста.

        :param video_id: id видео
        :param playlist_id: id плейлиста
        """
        super().__init__(video_id)

        self.playlist_id = playlist_id
