<script lang="ts" setup>
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
</script>

<template>
    <tr>
        <th scope="row">
            <i v-if="props.isFavorite" class="bi bi-heart-fill" @click="() => changeFavorite(props.uuid)"></i>
            <i v-else class="bi bi-heart" @click="() => changeFavorite(props.uuid)"></i>
        </th>
        <td>
            <a v-bind:href="youtubeURL">{{ props.name }}</a>
            <i v-if="props.isFull" class='bi bi-star'></i>
        </td>
        <td>{{ props.artist }}</td>
    </tr>
</template>
