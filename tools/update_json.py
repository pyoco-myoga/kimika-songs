import json
import uuid
from typing import Any, Dict, List, Set
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def get_all_artists(data: Dict[str, Any]) -> List[str]:
    artists = list(data.keys())
    return artists

def get_all_songs(data: Dict[str, Any]) -> Set[str]:
    songs = set()
    for artist in data.keys():
        songs = songs.union(set(song["name"] for song in data[artist]))
    return songs

def get_all_videos(data: Dict[str, Any]) -> Set[str]:
    videos = set()
    for artist in data.keys():
        videos = videos.union(set(song["video"] for song in data[artist]))
    return videos

def ls_artists(data: Dict[str, Any]):
    for artist in data.keys():
        print(artist)

def ls_song(data: Dict[str, Any]):
    for artist in data.keys():
        songs = set(song["name"] for song in data[artist])
        for song in songs:
            print(song)

def add_command(data: Dict[str, Any]) -> Dict[str, Any]:
    artists = get_all_artists(data)
    artists_completer = WordCompleter(artists)
    artist = prompt("artist> ", completer=artists_completer)

    songs = get_all_songs(data)
    songs_completer = WordCompleter(list(songs))
    song = prompt("song> ", completer=songs_completer)

    videos = get_all_videos(data)
    videos_completer = WordCompleter(list(videos))
    video = prompt("video> ", completer=videos_completer)

    t = int(prompt("t> "))
    endt = int(prompt("endt> "))

    length_completer = WordCompleter(["full", "short"])
    try:
        length = prompt("length> ", completer=length_completer)
    except EOFError:
        length = None

    singtype_completer = WordCompleter(["live", "known", "improvised", "shorts", "movie"])
    try:
        sing_type = prompt("singType> ", completer=singtype_completer)
    except EOFError:
        sing_type = None


    data.setdefault(artist, [])
    song_info = {
        "uuid": str(uuid.uuid4()),
        "name": song,
        "video": video,
        "t": t,
        "endt": endt,
        **({"length": length} if length is not None else {}),
        **({"singType": sing_type} if sing_type is not None else {})
        }
    data[artist].append(song_info)

    json_str = json.dumps(song_info, ensure_ascii=False, sort_keys=True, indent=4)
    print(f"{artist}: {json_str}")
    return data

def write_command(data: Dict[str, Any]):
    with open("./src/songs.json", "w", encoding="utf8") as f:
        f.write(
            json.dumps(
                data,
                ensure_ascii=False,
                sort_keys=True,
                indent=4))


if __name__ == "__main__":
    with open("./src/songs.json", encoding="utf8") as f:
        data = json.load(f)

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

