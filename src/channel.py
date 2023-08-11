import json
import os
from typing import Any

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.environ.get("YT_API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        channel = (
            self.youtube.channels()
            .list(id=channel_id, part="snippet,statistics")
            .execute()
        )
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.video_count = channel["items"][0]["statistics"]["viewCount"]
        self.subscriber_count: int = channel["items"][0]["statistics"][
            "subscriberCount"
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, other: int):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other: int):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other: int):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __gt__(self, other: int):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __le__(self, other: int):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __ge__(self, other: int):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other: int):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.channel = (
            self.youtube.channels()
            .list(id=self.channel_id, part="snippet,statistics")
            .execute()
        )
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @staticmethod
    def get_service():
        api_key: str = os.getenv("YT_API_KEY")
        return build("youtube", "v3", developerKey=api_key)

    def to_json(self, file):
        self.file = file
        attrib_dict = {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "video_count": self.video_count,
        }
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(attrib_dict, f, indent=2, ensure_ascii=False)
