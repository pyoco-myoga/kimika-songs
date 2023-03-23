
// import songs from "./songs.json";
// import $ from "jquery";
// import Fuse from "fuse.js";
import {getCookie, setCookie} from "typescript-cookie";
// import {Song} from "./@types";

import { createApp } from "vue";
import App from "./App.vue";

const app = createApp(App);
app.mount("#app");

// const FAVORITE_SONGS_COOKIE_KEY = "favorite";
// const COOKIE_EXPIRES = 161 * 365
// const MAX_NUM_FAVORITE_SONGS = 50;
//
// let songsList: {artist: string, song: Song}[] = [];
// for (const artist of Object.keys(songs)) {
//     for (const song of songs[artist]) {
//         songsList.push({
//             artist,
//             song: song as Song,
//         });
//     }
// }
// const fuse = new Fuse(songsList, {
//     shouldSort: true,
//     threshold: 0.4,
//     keys: [
//         "artist",
//         "song.name"
//     ]
// });
//
// function addTableRow(item: {artist: string, song: Song}, favoriteSongs: Set<string>, videoId: string) {
//     const isFavorite = favoriteSongs.has(item.song.uuid);
//     if ($("#favorite-only").prop("checked")) {
//         if (!isFavorite) {
//             return;
//         }
//     }
//     const isFull = item.song.length === "full";
//     if ($("#full-only").prop("checked")) {
//         if (!isFull) {
//             return;
//         }
//     }
//     if (videoId !== "" && videoId !== item.song.video) {
//         return;
//     }
//     $("#songs-list").append(`
//     <tr>
//         <th scope="row">
//             <i id="${item.song.uuid}" class="bi ${(isFavorite) ? "bi-heart-fill" : "bi-heart"}"></i>
//         </th>
//         <td>
//             <a href="https://www.youtube.com/watch?v=${item.song.video}&t=${item.song.t}">${item.song.name}</a>
//             ${(item.song.length === "full") ? "<i class='bi bi-star'></i>" : ""}
//         </td>
//         <td>${item.artist}</td>
//     </tr>
//     `);
// }
//
// function keyupEventHandler(favoriteSongs: Set<string>, keyword: string | null, videoId: string) {
//     $("#songs-list").empty();
//     if (keyword != null && keyword != "") {
//         for (const result of fuse.search(keyword)) {
//             addTableRow(result.item, favoriteSongs, videoId);
//             addFavoriteButtonEvent(result.item.song.uuid, favoriteSongs);
//         }
//     } else {
//         for (const item of songsList) {
//             addTableRow(item, favoriteSongs, videoId);
//             addFavoriteButtonEvent(item.song.uuid, favoriteSongs);
//         }
//     }
// }
//
// function addFavoriteButtonEvent(uuid: string, favoriteSongs: Set<string>) {
//     // if #uuid exists, event will be handled
//     $(`#${uuid}`).click(function () {
//         if ($(this).hasClass("bi-heart")) {
//             if (favoriteSongs.size < MAX_NUM_FAVORITE_SONGS) {
//                 favoriteSongs.add(uuid);
//                 setCookie(
//                     FAVORITE_SONGS_COOKIE_KEY,
//                     JSON.stringify([...favoriteSongs]), {expires: COOKIE_EXPIRES, sameSite: "strict"});
//                 $(this).removeClass("bi-heart").addClass("bi-heart-fill");
//             }
//         } else {
//             favoriteSongs.delete(uuid);
//             setCookie(
//                 FAVORITE_SONGS_COOKIE_KEY,
//                 JSON.stringify([...favoriteSongs]), {expires: COOKIE_EXPIRES, sameSite: "strict"});
//             $(this).removeClass("bi-heart-fill").addClass("bi-heart");
//         }
//     });
// }
//
// let favoriteSongsUUID = new Set<string>();
// const cookieString = getCookie(FAVORITE_SONGS_COOKIE_KEY);
//
// if (cookieString !== undefined) {
//     favoriteSongsUUID = new Set<string>(JSON.parse(cookieString));
// }
//
// // initialize
// $(() => {
//     const params = new URLSearchParams(location.search);
//     $("#search-query").val(params.get("q"));
//     keyupEventHandler(favoriteSongsUUID, params.get("q"), $("#video-id-specify").val() as string);
//
//     $("#search-query").on("keyup", () => keyupEventHandler(favoriteSongsUUID, $("#search-query").val() as string, $("#video-id-specify").val() as string));
//     $("#favorite-only").on("change", () => keyupEventHandler(favoriteSongsUUID, $("#search-query").val() as string, $("#video-id-specify").val() as string));
//     $("#full-only").on("change", () => keyupEventHandler(favoriteSongsUUID, $("#search-query").val() as string, $("#video-id-specify").val() as string));
//     $("#video-id-specify").on("keyup", () => keyupEventHandler(favoriteSongsUUID, $("#search-query").val() as string, $("#video-id-specify").val() as string));
// });
//
