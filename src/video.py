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

        self.video_title: str = video_response['items'][0]['snippet']['title']  # название видео
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']  # ссылка на видео
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']  # количество просмотров
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']  # количество лайков
