from googleapiclient.discovery import build

import json
import os
from typing import Any


class Video:
    api_key: str = os.environ.get("YT_API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, id_video) -> None:
        try:
            self.id_video = id_video
            self.channel = (
                self.youtube.videos()
                .list(id=id_video, part="snippet,statistics")
                .execute()
            )
            self.title = self.channel["items"][0]["snippet"]["title"]
            self.url_video = f"https://www.youtube.com/watch?v={self.id_video}"
            self.views = self.channel["items"][0]["statistics"]["viewCount"]
            self.like_count = self.channel["items"][0]["statistics"]["likeCount"]

        except IndexError:
            self.title = None
            self.like_count = None
            self.views = None
            self.url_video = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, id_video, playlist_id) -> None:
        super().__init__(id_video)
        self.playlist_id = playlist_id

    def __str__(self):
        return self.title
