from googleapiclient.discovery import build
from datetime import timedelta, datetime
import isodate

import os
from typing import Any


class PlayList:
    api_key: str = os.environ.get("YT_API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, pl_id) -> None:
        self.pl_id = pl_id
        self.url = f"https://www.youtube.com/playlist?list={pl_id}"
        self.playlist_video = (
            self.youtube.playlists().list(id=pl_id, part="snippet").execute()
        )
        self.title = self.playlist_video["items"][0]["snippet"]["title"]
        self.playlist_videos = (
            self.youtube.playlistItems()
            .list(playlistId=self.pl_id, part="contentDetails", maxResults=50)
            .execute()
        )

        self.video_ids: list[str] = [
            video["contentDetails"]["videoId"]
            for video in self.playlist_videos["items"]
        ]
        self.video_response = (
            self.youtube.videos()
            .list(id=",".join(self.video_ids), part="contentDetails, statistics")
            .execute()
        )

    @property
    def total_duration(self):
        all_time = timedelta(seconds=0)

        for video in self.video_response["items"]:
            duration_inv = video["contentDetails"]["duration"]
            duration = isodate.parse_duration(duration_inv)
            all_time += duration

        return all_time

    def show_best_video(self):
        i = 0
        max_like = 0

        for items in self.video_response:
            likes_video = int(
                self.video_response["items"][i]["statistics"]["likeCount"]
            )
            if max_like < likes_video:
                url_best_video = self.video_response["items"][i]["id"]
            i += 1

        return f"https://youtu.be/{url_best_video}"
