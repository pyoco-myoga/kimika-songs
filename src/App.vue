<script lang="ts">
const params = new URLSearchParams(location.search);
const q = params.get("q");
</script>

<script lang = "ts" setup>
import SongTable from "./components/SongTable.vue";
import Header from "./components/Header.vue";
import {ref} from "vue";

const keyword = ref(q !== null ? q : "");
const isFavoriteOnly = ref(false);
const isFullOnly = ref(false);
const videoIdSpecify = ref("");
</script>

<template>
    <notifications position="bottom right" />
    <Header />
    <div class="input-group mb-2">
        <span class="input-group-text">
            <i class="bi bi-search"></i>
        </span>
        <input v-model="keyword" class="form-control" placeholder="キーワードであいまい絞り込み">
    </div>
    <div>

        <div class="input-group mb-2">
            <span class="input-group-text">検索オプション</span>
            <input v-model="isFavoriteOnly" id="favorite-only" class="btn-check" type="checkbox" autocomplete="off">
            <label class="btn btn-outline-secondary" for="favorite-only"><i class="bi bi-heart-fill" />のみ</label>

            <input v-model="isFullOnly" id="full-only" class="btn-check" type="checkbox" autocomplete="off">
            <label class="btn btn-outline-secondary" for="full-only">フルのみ</label>
        </div>

        <div class="input-group mb-3">
            <span class="input-group-text" id="video-id-specify-label">video ID</span>
            <input v-model="videoIdSpecify" type="text" class="form-control" aria-describedby="video-id-specify-label"
                placeholder="YouTubeリンク または video ID">
        </div>
    </div>
    <SongTable :keyword="keyword" :video-id="videoIdSpecify" :is-full-only="isFullOnly"
        :is-favorite-only="isFavoriteOnly" />
</template>
