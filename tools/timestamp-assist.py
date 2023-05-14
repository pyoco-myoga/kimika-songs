from datetime import datetime
import os
import pickle
from typing import Any, List, Optional, Tuple
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, base
import pyperclip

TMP_FILE = "/tmp/timestamp.pkl"

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
    video_id: Optional[str] = None
    base_time: Optional[datetime] = None
    data: List[Tuple[datetime, datetime, str]] = []
    command_completer = WordCompleter([
        "ls", "add", "pop", "timestamp", "url", "base", "video", "write", "load"
        ])
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
            for (t, endt, song_artist) in data:
                timestamp_str += \
                        f"{datetime_to_time(t, base_time)} " \
                        f"{datetime_to_time(endt, base_time)} " \
                        f"{song_artist}\n"
            print(timestamp_str)
            pyperclip.copy(timestamp_str)

        elif cmd[0] == "add":
            dt = datetime.now()
            song_artist = prompt("endt and (song, artist)>")
            data.append((dt, datetime.now(), song_artist))

        elif cmd[0] == "pop":
            print(data.pop())

        elif cmd[0] == "timestamp":
            if base_time is None:
                print("base_time is not set, please set")
                continue
            timestamp_str = ""
            for (t, _endt, song_artist) in data:
                timestamp_str += f"{datetime_to_time(t, base_time)} {song_artist}\n"
            print(timestamp_str)
            pyperclip.copy(timestamp_str)

        elif cmd[0] == "url":
            if base_time is None:
                print("base_time is not set, please set")
                continue
            if video_id is None:
                print("video_id is not set, please set")
                continue
            for (t, endt, song_artist) in data:
                delta = t - base_time
                print(song_artist)
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

        else:
            print(f"not supported command {cmd[0]}")
