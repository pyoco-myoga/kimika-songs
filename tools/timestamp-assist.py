import os
import pickle
import json
from datetime import datetime
from typing import Any, List, Optional, Tuple

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, base
import pyperclip

import update_json
from update_json import SongInfo, ExtendedJSONEncoder

TMP_FILE = "/tmp/timestamp.pkl"
COMMAND_LIST = [
    "ls", "add", "pop", "timestamp", "url", "base", "video", "write", "load"
]

def write_command(data: List[Any], video_id: str, base_time: datetime):
    with open(TMP_FILE, "wb") as f:
        pickle.dump((data, video_id, base_time), f)

def load_command() -> Optional[Tuple[List[Any], str, datetime]]:
    if not os.path.exists(TMP_FILE):
        return None
    with open(TMP_FILE, "rb") as f:
        data, video_id, base_time = pickle.load(f)
    return data, video_id, base_time


def youtube_url(video_id: str, second: int) -> str:
    return f"https://youtube.com/watch?v={video_id}&t={second}"


def datetime_to_time(t: datetime, base: datetime) -> str:
    delta = t - base
    hours = delta.seconds // 3600
    minutes = (delta.seconds // 60) % 60
    seconds = delta.seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


if __name__ == "__main__":
    with open("./src/songs.json", encoding="utf8") as f:
        songs_data = {
            artist: [SongInfo(**song_info) for song_info in song_infos]
            for artist, song_infos in json.load(f).items()}

    video_id: Optional[str] = None
    base_time: Optional[datetime] = None
    data: List[Tuple[datetime, datetime, str, SongInfo]] = []
    command_completer = WordCompleter(COMMAND_LIST)
    while True:
        try:
            cmd = prompt("> ", completer=command_completer).split()
        except EOFError:
            if input("exit? y/n>") == "y":
                break
            else:
                continue

        if len(cmd) == 0:
            continue

        if cmd[0] == "ls":
            if base_time is None:
                print("base_time is not set, please set")
                continue
            timestamp_str = ""
            for (t, endt, artist, song_info) in data:
                timestamp_str += \
                        f"{datetime_to_time(t, base_time)} " \
                        f"{datetime_to_time(endt, base_time)} " \
                        f"{song_info.name} / {artist}\n"
            print(timestamp_str)
            pyperclip.copy(timestamp_str)

        elif cmd[0] == "add":
            dt = datetime.now()
            artist, song_info = update_json.input_song_info(songs_data)
            data.append((dt, datetime.now(), artist, song_info))

        elif cmd[0] == "pop":
            print(data.pop())

        elif cmd[0] == "timestamp":
            if base_time is None:
                print("base_time is not set, please set")
                continue
            timestamp_str = ""
            for (t, _endt, artist, song_info) in data:
                timestamp_str += f"{datetime_to_time(t, base_time)} {song_info.name} / {artist}\n"
            print(timestamp_str)
            pyperclip.copy(timestamp_str)

        elif cmd[0] == "url":
            if base_time is None:
                print("base_time is not set, please set")
                continue
            if video_id is None:
                print("video_id is not set, please set")
                continue
            for (t, endt, artist, song_info) in data:
                delta = t - base_time
                print(artist, " / ", song_info.name)
                print(f"t: {youtube_url(video_id, int(delta.total_seconds()))}")
                delta = endt - base_time
                print(f"t: {youtube_url(video_id, int(delta.total_seconds()))}")
                print()

        elif cmd[0] == "base":
            base = prompt(
                "base> ",
                default=str((base_time or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")))
            try:
                base_time = datetime.strptime(base, "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                print(e)
            continue

        elif cmd[0] == "video":
            video_id = prompt("video id> ")

        elif cmd[0] == "write":
            if base_time is None:
                print("base_time is not set, please set")
                continue
            if video_id is None:
                print("video_id is not set, please set")
                continue
            write_command(data, video_id, base_time)

        elif cmd[0] == "load":
            result = load_command()
            if result is not None:
                data, video_id, base_time = result

        elif cmd[0] == "json":
            print(data)
            pyperclip.copy(json.dumps(
                data,
                ensure_ascii=False,
                sort_keys=True,
                indent=4,
                cls=ExtendedJSONEncoder))

        else:
            print(f"not supported command {cmd[0]}")
