
<script lang="ts">
import Fuse from "fuse.js";
import {getCookie, setCookie} from 'typescript-cookie';
import songs from "../songs.json";
import {Song} from "../@types";

const COOKIE_EXPIRES = 161 * 365;
const FAVORITE_SONGS_COOKIE_KEY = "favorite";
const MAX_NUM_FAVORITE_SONGS = 50;

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
</script>

<script lang="ts" setup>
import SongRow from './SongRow.vue';
import {ref} from 'vue';
const props = defineProps<{
    keyword: string,
    videoId: string,
    isFullOnly: boolean,
    isFavoriteOnly: boolean,
}>();

const cookieString = getCookie(FAVORITE_SONGS_COOKIE_KEY)
let favoriteSongsUUID = ref(new Set<string>((cookieString !== undefined) ? JSON.parse(cookieString) : []));

const addOrRemoveFavorite = (uuid: string) => {
    if (favoriteSongsUUID.value.has(uuid)) {
        favoriteSongsUUID.value.delete(uuid);
    } else {
        if (favoriteSongsUUID.value.size < MAX_NUM_FAVORITE_SONGS) {
            favoriteSongsUUID.value.add(uuid);
        }
    }
    setCookie(
        FAVORITE_SONGS_COOKIE_KEY,
        JSON.stringify([...favoriteSongsUUID.value]), {expires: COOKIE_EXPIRES, sameSite: "strict"});
};

const isVideoIdRegex = /^[a-zA-Z0-9_-]{11}$/;
const extractVideoIdRegex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/)|youtu\.be\/|youtube\.com\/shorts\/)([^\s&?]+)/;

const isDisplay = (song: Song): boolean => {
    if (props.isFullOnly && song.length !== "full") {
        return false;
    }
    if (props.isFavoriteOnly && !favoriteSongsUUID.value.has(song.uuid)) {
        return false;
    }
    if (props.videoId === "") {
        return true;
    }

    if (isVideoIdRegex.test(props.videoId) && song.video !== props.videoId) {
        return false;
    }
    const match = props.videoId.match(extractVideoIdRegex);
    if (match && match.length >= 1 && song.video !== match[1]) {
        return false;
    }
    return true;
};
</script>

<template>
    <table class="table table-striped table-bordered">
        <thead>
            <tr>
                <th scope="col">お気に入り ({{ favoriteSongsUUID.size }}/{{ MAX_NUM_FAVORITE_SONGS }})</th>
                <th scope="col">曲 (<i class="bi bi-star"></i>はフル、それ以外は不明)</th>
                <th scope="col">アーティスト</th>
            </tr>
        </thead>
        <tbody>
            <template v-if="props.keyword === ''">
                <template v-for="{artist, song} of songsList" :key="song.uuid">
                    <template v-if="isDisplay(song)">
                        <SongRow :uuid="song.uuid" :video="song.video" :artist="artist" :name="song.name" :t="song.t"
                            :is-favorite="favoriteSongsUUID.has(song.uuid)" :is-full="song.length === 'full'"
                            @change-favorite-event="addOrRemoveFavorite" />
                    </template>
                </template>
            </template>
            <template v-else>
                <template v-for="result of fuse.search(props.keyword)" :key="result.item.song.uuid">
                    <template v-if="isDisplay(result.item.song)">
                        <SongRow :uuid="result.item.song.uuid" :video="result.item.song.video" :artist="result.item.artist"
                            :name="result.item.song.name" :t="result.item.song.t"
                            :is-favorite="favoriteSongsUUID.has(result.item.song.uuid)"
                            :is-full="result.item.song.length === 'full'" @change-favorite-event="addOrRemoveFavorite" />
                    </template>
                </template>

            </template>
        </tbody>
    </table>
</template>
