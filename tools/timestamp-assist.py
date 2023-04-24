from datetime import datetime
from typing import List, Optional
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, base
import pyperclip


def write_command(data: List[datetime]):
    with open("./timestamp-data.txt", "w", encoding="utf8") as f:
        f.write(str(data))


if __name__ == "__main__":
    video_id: Optional[str] = None
    base_time: Optional[datetime] = None
    data: List[datetime] = []
    command_completer = WordCompleter(["ls", "append", "pop", "timestamp", "url", "base"])
    while True:
        try:
            cmd = prompt("> ").split()
        except EOFError:
            break
        if len(cmd) == 0:
            continue

        if cmd[0] == "exit":
            break

        if cmd[0] == "ls":
            for t in data:
                print(t)
        elif cmd[0] == "append":
            dt = datetime.now()
            data.append(dt)
        elif cmd[0] == "pop":
            print(data.pop())

        elif cmd[0] == "timestamp":
            if base_time is None:
                print("base_time is not set, please set")
                continue
            timestamp_str = ""
            for t in data:
                delta = t - base_time
                hours = delta.seconds // 3600
                minutes = (delta.seconds // 60) % 60
                seconds = delta.seconds % 60
                timestamp = f"{hours:02}:{minutes:02}:{seconds:02}"
                timestamp_str += timestamp + "\n"
            print(timestamp_str)
            pyperclip.copy(timestamp_str)

        elif cmd[0] == "url":
            if base_time is None:
                print("base_time is not set, please set")
                continue
            if video_id is None:
                print("video_id is not set, please set")
                continue
            for t in data:
                delta = t - base_time
                print(f"https://youtube.com/watch?v={video_id}&t={int(delta.total_seconds())}")

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
        else:
            print(f"not supported command {cmd[0]}")

    write_command(data)
