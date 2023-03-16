
import songs from "./songs.json";
import $ from "jquery";
import Fuse from "fuse.js";
import {Song} from "./@types";

let songsList: {artist: string, song: Song}[] = [];
for (const artist of Object.keys(songs)) {
    for (const song of songs[artist]) {
        songsList.push({
            artist,
            song: song as Song,
        });
    }
}
const fuse = new Fuse(songsList, {
    shouldSort: true,
    threshold: 0.4,
    keys: [
        "artist",
        "song.name"
    ]
});

function eventHandler() {
    $("#songs-list").empty();
    if ($("#search-query").val() !== "") {
        for (const result of fuse.search($("#search-query").val() as string)) {
            $("#songs-list").append(`
            <tr>
                <th scope="row">${result.item.artist}</th>
                <td><a href="https://www.youtube.com/watch?v=${result.item.song.id}&t=${result.item.song.t}">${result.item.song.name}</th>
            </tr>
    `);
        }
    } else {
        for (const item of songsList) {
            $("#songs-list").append(`
            <tr>
                <th scope="row">${item.artist}</th>
                <td><a href="https://www.youtube.com/watch?v=${item.song.id}&t=${item.song.t}">${item.song.name}</th>
            </tr>
            `);
        }
    }
}


// initialize
$(() => {
    for (const item of songsList) {
        $("#songs-list").append(`
        <tr>
            <th scope="row">${item.artist}</th>
            <td><a href="https://www.youtube.com/watch?v=${item.song.id}&t=${item.song.t}">${item.song.name}</th>
        </tr>
        `);
        console.log(item);
    }
});

$("#search-query").on("keyup", eventHandler);


