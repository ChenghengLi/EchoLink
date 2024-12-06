<template>
	<div class="rounded">
        <div class="flex items-center echolink-container">

            <!-- Song icon (would be ex. album cover) -->
            <!-- min-w is necessary to avoid the box being compressed if title is too long -->
            <div class="flex size-10 min-w-10 rounded bg-indigo-400">
                <MusicalNoteIcon class="icon-h5 my-auto mx-auto"/>
            </div>

            <!-- Artist & title -->
            <span class="mx-3 text-left">
                {{ prefix ? prefix : ''}} <router-link :to="`/users/${song.artist_name}`">{{ song.artist_name }}</router-link> - <router-link :to="`/songs/${song.song_id}`">{{  song.title }}</router-link>
            </span>

            <div class="mx-auto"></div>

            <!-- TODO readd when we get duration field -->
            <!-- <span class="mx-3">{{ duration }}</span> -->
            <span class="mx-3" v-tooltip="'Genre'">{{ song.genre }}</span>

            <!-- Edition controls -->
            <!-- TODO how the fuck could reorder be made accessible? -->
            <Bars3Icon v-if="showHandle" class="icon handle mx-3" />
            <button v-if="showDelete" class="btn btn-delete text-nowrap p-2" @click="$emit('removed', song)">
                <TrashIcon class="icon-h5" />
            </button>
        </div>
    </div>
</template>

<script setup>
import { MusicalNoteIcon, TrashIcon, Bars3Icon } from '@heroicons/vue/24/solid'

defineProps({
    "song": Object, // TODO adjust all usages once specs are final
    "showHandle": Boolean, // Whether to show a drag handle.
    "showDelete": Boolean, // Whether to show a delete button.
    "prefix": String, // String to prefix before artist and title.
})

// TODO readd once we add song durations to API
// const duration = computed(() => {``
//     let seconds = `${props.song.duration % 60}`
//     seconds = seconds.padStart(3 - seconds.length, 0)
//     return `${Math.floor(props.song.duration / 60)}:${seconds}` // Assumes duration is in seconds
// })

</script>

<style scoped>

.btn {
    @apply font-bold rounded;
}

.btn-delete {
    @apply bg-blue-500 text-white;
}

.btn-delete:hover,
.btn-delete:focus {
    @apply bg-red-700;
}

.handle {
    cursor: pointer;
}

</style>
