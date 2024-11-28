<template>
    <div class="home-two-light home-light container">
        <HeaderComponent />
        <div class="mx-auto w-100">
            <!-- TODO welcome back message -->

            <!-- Latest tracks -->
            <div class="px-4 mx-auto">
                <h2>Explore tracks</h2>
                <p>Be the first to hear what's new on EchoLink, or find new tracks from your favourite genres.</p>

                <div v-if="songsError === null" class="flex flex-col-reverse lg:flex-row content-center w-100">
                    <!-- I actually have no idea why I cannot get the children to be centered. Had to rely on this ugly hack of having 2 growing elems on the sides. TODO -->
                    <div class="flex-grow"/>

                    <!-- Song list -->
                    <div class="flex flex-col items-center flex-grow">
                        <!-- TODO if empty, show message -->
                        <SongList v-model="shownSongs" :editable=false />
                        <button v-if="shownSongsAmount <= songs.length" class="btn btn-blue w-32 mt-2" @click="showMoreSongs"> <!-- Don't show the button if all tracks are already being shown. -->
                            <PlusIcon class="icon" />
                            Show more
                        </button>
                    </div>

                    <div class="mx-2 my-2"/> <!-- Spacing -->

                    <!-- Search and filters -->
                    <div class="content-block max-h-min flex-grow max-w-lg">
                        <p class="section-header mb-2">Filter</p>
                        
                        <TextInput label="Search" placeholder="Search by name or artist..." input-type="text" :value="search.text" @changed="search.text = $event"></TextInput>

                        <OptionSelector v-model="search.genre" :options="genres" label="Genre" track-by="id" option-label-key="label" :allow-empty="true" :can-search="true"></OptionSelector>
                    </div>

                    <div class="flex-grow"/>
                </div>
                <p v-else class="text-gray-500">Something went wrong while fetching latest songs:<br>{{ songsError }}.<br>Try refreshing the page.</p>

                <hr class="h-divider"/>
            </div>

            <!-- Browse artists -->
            <div class="mx-auto">
                <h2>Explore artists</h2>
                <p>Connect with your favorite musicians on EchoLink.</p>

                <ArtistsList/>
            </div>

        </div>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import { PlusIcon } from '@heroicons/vue/24/solid'
import OptionSelector from '../components/form/OptionSelector.vue';
import ArtistsList from '../components/ArtistsList.vue';
import SongList from '../components/SongList.vue';
import SongService from '../services/song.js'
import { computed, ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const LATEST_SONGS_STEP = 5 // Amount of additional songs to display when clicking "Show more"

const songs = reactive([])
const songsError = ref(null)
const shownSongsAmount = ref(3) // Ref in case we decide to make it customizable.
const genres = reactive([])
const registeredGenres = ref(new Set())

const search = reactive({
    genre: null,
    text: '',
})

async function fetchSongs() {
    try {
        const newData = await SongService.getAll()
        for (const index in newData.songs) {
            const song = newData.songs[index]

            // Add an extra field to improve vue-multiselect search support (since it only supports searching by one key)
            song.fullTitle = `${song.artist} - ${song.title}`

            // Track all used genres
            if (!registeredGenres.value.has(song.genre)) {
                genres.push({id: song.genre, label: song.genre})
                registeredGenres.value.add(song.genre)
            }
        }
        Object.assign(songs, newData.songs)
    } catch (err) {
        songsError.value = (err.response) ? err.response.data.detail : err.message
    }
}

function showMoreSongs() {
    shownSongsAmount.value += LATEST_SONGS_STEP
}

const shownSongs = computed(() => {
    console.log(search.genre)
    let results = songs.filter((song) => {
        return (search.text === '' || song.fullTitle.includes(search.text)) && (search.genre === null || search.genre.id === song.genre)
    })
    results = results.slice(0, shownSongsAmount.value)
    return results
})

// Fetch song data when the page is accessed.
onMounted(function () {
    fetchSongs()
})

</script>


<style scoped>
.container {
    width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align items to the top */
    min-height: 100vh; /* Ensure the container takes the full height of the viewport */
}

.content-block {
    @apply p-4 border-2 rounded-lg border-indigo-100 bg-indigo-200
}

.footer-light {
    width: 100vw;
}
.section-header {
    @apply text-left font-bold text-xl
}

.btn-blue {
    @apply font-bold py-3 px-4 rounded;
    @apply bg-blue-500 text-white;
    @apply text-nowrap mb-2
}

.btn-blue:hover,
.btn-blue:focus {
    @apply bg-blue-700;
}

</style>