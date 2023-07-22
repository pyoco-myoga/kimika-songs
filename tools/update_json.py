import dataclasses
from enum import Enum
import json
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

COMMAND_LIST = [
    "ls",
    "add",
    "write",
    "exit"
]

class LengthEnum(str, Enum):
    full = "full"
    short = "short"

class SingTypeEnum(str, Enum):
    live = "live"
    known = "known"
    improvised = "improvised"
    shorts = "shorts"
    movie = "movie"

@dataclass
class SongInfo:
    uuid: str
    name: str
    video: str
    t: int
    endt: Optional[int] = None
    length: Optional[LengthEnum] = None
    singType: Optional[SingTypeEnum] = None

class ExtendedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SongInfo):
            return dataclasses.asdict(obj)
        return json.JSONEncoder.default(self, obj)


def time_to_second(time_str: str) -> int:
    """
    time_str: str
        [[[%H:]%M:]%S]
    """
    time_parts = time_str.split(":") if len(time_str) > 0 else []
    hours = int(time_parts[-3]) if len(time_parts) == 3 else 0
    minutes = int(time_parts[-2]) if len(time_parts) >= 2 else 0
    seconds = int(time_parts[-1]) if len(time_parts) >= 1 else 0
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds

def get_all_artists(data: Dict[str, List[SongInfo]]) -> List[str]:
    artists = list(data.keys())
    return artists

def get_all_songs(data: Dict[str, List[SongInfo]]) -> Set[str]:
    songs = set()
    for artist in data.keys():
        songs = songs.union(set(song.name for song in data[artist]))
    return songs

def get_all_videos(data: Dict[str, List[SongInfo]]) -> Set[str]:
    videos = set()
    for artist in data.keys():
        videos = videos.union(set(song.video for song in data[artist]))
    return videos

def ls_artists(data: Dict[str, List[SongInfo]]):
    for artist in data.keys():
        print(artist)

def ls_song(data: Dict[str, List[SongInfo]]):
    for artist in data.keys():
        songs = set(song.name for song in data[artist])
        for song in songs:
            print(song)


def input_song_info(data: Dict[str, List[SongInfo]]) -> Tuple[str, SongInfo]:
    artists = get_all_artists(data)
    artists_completer = WordCompleter(artists)
    artist = prompt("artist> ", completer=artists_completer)

    songs_completer = WordCompleter(
            list(
                map(
                    lambda x: x.name,
                    data.get(artist, []))))
    song = prompt("song> ", completer=songs_completer)

    videos = get_all_videos(data)
    videos_completer = WordCompleter(list(videos))
    video = prompt("video> ", completer=videos_completer)

    t = time_to_second(prompt("t> "))
    endt = time_to_second(prompt("endt> "))

    length_completer = WordCompleter([x.value for x in LengthEnum])
    try:
        length = prompt("length> ", completer=length_completer)
        length = LengthEnum[length]
    except KeyError:
        print("Warning: KeyError")
        length = None
    except EOFError:
        length = None

    singtype_completer = WordCompleter([x.value for x in SingTypeEnum])
    try:
        sing_type = prompt("singType> ", completer=singtype_completer)
        sing_type = SingTypeEnum[sing_type]
    except KeyError:
        print("Warning: KeyError")
        sing_type = None
    except EOFError:
        sing_type = None

    song_info = SongInfo(
        uuid=str(uuid.uuid4()),
        name=song,
        video=video,
        t=t,
        endt=endt,
        length=length,
        singType=sing_type)
    return artist, song_info

def add_command(data: Dict[str, List[SongInfo]]) -> Dict[str, List[SongInfo]]:

    artist, song_info = input_song_info(data)
    data.setdefault(artist, [])
    data[artist].append(song_info)
    data[artist].sort(key=lambda x: x.name)

    json_str = json.dumps(
        song_info,
        ensure_ascii=False,
        sort_keys=True,
        indent=4,
        cls=ExtendedJSONEncoder)
    print(f"{artist}: {json_str}")
    return data

def write_command(data: Dict[str, List[SongInfo]]):
    with open("./src/songs.json", "w", encoding="utf8") as f:
        f.write(
            json.dumps(
                data,
                ensure_ascii=False,
                sort_keys=True,
                indent=4,
                cls=ExtendedJSONEncoder))


if __name__ == "__main__":
    with open("./src/songs.json", encoding="utf8") as f:
        data = {
            artist: [SongInfo(**song_info) for song_info in song_infos]
            for artist, song_infos in json.load(f).items()}

    while True:
        try:
            command_completer = WordCompleter(COMMAND_LIST)
            cmd = prompt("> ", completer=command_completer).split()
        except EOFError:
            break
        if len(cmd) == 0:
            continue
        if cmd[0] == "exit":
            break

        if cmd[0] == "ls":
            if len(cmd) == 1:
                print("ls command has subcommand, `artist`, `song`")
                continue
            if cmd[1] == "artist":
                ls_artists(data)
            elif cmd[1] == "song":
                ls_song(data)
        elif cmd[0] == "add":
            data = add_command(data)
        elif cmd[0] == "write":
            write_command(data)
        else:
            print(f"not supported command {cmd[0]}")

    write_command(data)

