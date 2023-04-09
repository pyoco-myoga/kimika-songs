<script lang="ts" setup>
import * as vue from "vue";
import {notify} from '@kyvg/vue3-notification';
const props = defineProps<{
    uuid: string,
    video: string,
    artist: string,
    name: string,
    t: number,
    endt?: number,
    isFavorite: boolean,
    isFull: boolean,
}>();
const youtubeURL = `https://www.youtube.com/watch?v=${props.video}&t=${props.t}`;

// favorite mark: on/off
const emit = defineEmits(["changeFavoriteEvent"]);
const changeFavorite = (uuid: string): void => {
    emit("changeFavoriteEvent", uuid);
};

// behavior of share button
const shareButtonEvent = async () => {
    await navigator.clipboard.writeText(`${props.name} / ${props.artist}: ${youtubeURL}`);
    notify({title: `クリップボードにコピーしました<br>${props.name} / ${props.artist}`});
};

// expand youtube embed
const isExpandYoutubeEmbed = vue.ref(false);
const expandYoutubeEmbed = () => {
    isExpandYoutubeEmbed.value = !isExpandYoutubeEmbed.value;
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
                <a class="btn btn-outline-secondary" v-bind:href="youtubeURL">
                    <i class="bi bi-youtube text-danger" />
                </a>
                <a class="btn btn-outline-secondary" @click="shareButtonEvent">
                    <i class="bi bi-share text-info" />
                </a>
                <a class="btn btn-outline-secondary" @click="expandYoutubeEmbed">
                    <i class="bi bi-code-slash text-dark" />
                </a>
            </div>
            <div v-if="!props.endt && isExpandYoutubeEmbed" class="embed-responsive embed-responsive-16by9">
                <iframe type="text/html" class="embed-responsive-item"
                    v-bind:src="`https://www.youtube-nocookie.com/embed/${props.video}?enablejsapi=1&start=${props.t}`"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowfullscreen />
            </div>
        </td>
        <td>{{ props.artist }}</td>
    </tr>
</template>
