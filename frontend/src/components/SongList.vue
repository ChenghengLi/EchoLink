<template>
	<div class="w-100">
        <draggable v-model="songs" group="songs" @start="dragging=true" @end="dragging=false" item-key="id" handle=".handle">
            <template #item="{element}">
                <SongItem class="my-1" :song="element" :show-handle="props.editable" :show-delete="props.editable" :prefix="getSongPrefix(element)" @removed="removeSong($event)"></SongItem>
            </template>
        </draggable>
    </div>
</template>

<script setup>
import draggable from 'vuedraggable'
import SongItem from '../components/SongItem.vue'
import { ref } from 'vue';

const songs = defineModel({type: Array})

const props = defineProps({
    "editable": Boolean, // Whether songs can be reordered and deleted. Adding songs is an external responsibility.
})

const dragging = ref(false)

function getSongPrefix(song) {
    const index = songs.value.indexOf(song) + 1
    return `${index}.`
}

function removeSong(song) {
    // TODO maybe prompt the user first?
    songs.value.splice(songs.value.indexOf(song), 1)
}

</script>

<style scoped>

</style>
