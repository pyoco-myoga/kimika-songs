<script lang="ts" setup>
import {notify} from '@kyvg/vue3-notification';
const props = defineProps({
    uuid: String,
    video: String,
    artist: String,
    name: String,
    t: Number,
    isFavorite: Boolean,
    isFull: Boolean,
});
const youtubeURL = `https://www.youtube.com/watch?v=${props.video}&t=${props.t}`;

const emit = defineEmits(["changeFavoriteEvent"]);
const changeFavorite = (uuid: string): void => {
    emit("changeFavoriteEvent", uuid);
};
const shareButtonEvent = async () => {
    await navigator.clipboard.writeText(`[${props.name}(${props.artist})](${youtubeURL})`);
    notify({title: `クリップボードにコピーしました<br>${props.name}(${props.artist})`});
};
</script>

<template>
    <tr>
        <th scope="row">
            <i v-if="props.isFavorite" class="bi bi-heart-fill" @click="() => changeFavorite(props.uuid)"></i>
            <i v-else class="bi bi-heart" @click="() => changeFavorite(props.uuid)" />
        </th>
        <td>

            <a class="btn text-decoration-underline" v-bind:href="youtubeURL">
                {{ props.name }}
                <i v-if="props.isFull" class='bi bi-star' />
            </a>
            <div class="input-group mb-2">
                <a class="bi bi-youtube btn btn-outline-secondary" v-bind:href="youtubeURL" />
                <i class="bi bi-share btn btn-outline-secondary" @click="shareButtonEvent" />
            </div>
        </td>
        <td>{{ props.artist }}</td>
    </tr>
</template>
