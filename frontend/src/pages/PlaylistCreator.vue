<template>
    <div class="home-two-light home-light container">
        <HeaderComponent />
        
        <!-- Show a loading spinner while fetching user data -->
        <div v-if="!isLoaded" class="flex">
            <LoadingSpinner class="mx-auto" />
        </div>
        <!-- Set a fixed width for the container -->
        <div v-else-if="isLoaded && errorMsg === null" class="form-container relative mx-auto p-4 mt-8 border-3 rounded-lg border-indigo-100 bg-indigo-200">
            <div class="mb-3">
                <h2>{{ (isCreating() ? 'Create Playlist' : (isEditing ? 'Edit Playlist' : fullTitle)) }}</h2>
            </div>

            <!-- Edit button -->
            <div v-if="canEdit" class="absolute right-0 top-0 p-3 d-flex flex-column flex-md-row ml-auto mr-md-0">
                <button v-if="isEditing" class="btn btn-save" @click="saveChanges">
                    <PencilIcon class="icon" />
                    Save
                </button>
                <button v-else class="btn btn-edit" @click="isEditing = !isEditing">
                    <PencilIcon class="icon" />
                    Edit
                </button>
            </div>

            <!-- Form field container -->
            <div v-if="isCreating() || isEditing" class="px-4 mx-auto mb-4">
                <!-- Playlist name -->
                <TextInput label="Playlist Name" :required="true" placeholder="My playlist" input-type="text" :value="playlist.name" @changed="playlist.name = $event"></TextInput>

                <!-- Description -->
                <TextInput label="Description" placeholder="Describe your playlist..." input-type="text" :value="playlist.description" @changed="playlist.description = $event" :multiline="true" :max-length="DESCRIPTION_MAX_LENGTH"></TextInput>

                <!-- Visibility -->
                <OptionSelector v-model="playlist.visibility" :options="VISIBILITY_OPTIONS" label="Visibility" track-by="id" option-label-key="label" :allow-empty="false" :can-search="false"></OptionSelector>
            </div>
            <!-- Read-only details -->
            <div v-else class="px-4 mx-auto mb-3">
                <p>{{ playlist.description }}</p>
            </div>

            <!-- Song list; songs are added after creating a playlist, thus this doesn't appear in the creator view -->
            <SongList v-if="!isCreating()" v-model="playlist.songs" :editable="isEditing"></SongList>

            <!-- "Create" button -->
            <button v-if="isCreating()" class="btn btn--primary w-100 w-md-60 mt-3" :disabled="!canCreate" @click="createPlaylist">Create</button>
        </div>
        <ErrorPanel v-else header="The playlist could not be loaded:" :reason="errorMsg"></ErrorPanel>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import OptionSelector from '../components/form/OptionSelector.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';
import SongList from '../components/SongList.vue';
import ErrorPanel from '../components/ErrorPanel.vue';
import PlaylistService from '../services/playlist.js'
import UserService from '../services/user.js'
import Toast from '../utilities/toast.js'
import Swal from 'sweetalert2'
import { PencilIcon } from '@heroicons/vue/24/solid'
import { useRoute, useRouter } from 'vue-router';
import { computed, reactive, ref, watch, onMounted } from 'vue';

const router = useRouter()
const route = useRoute()

const DESCRIPTION_MAX_LENGTH = 120
// IDs be coherent with the API.
const VISIBILITY_OPTIONS = [
    {id: 'public', label: 'Public'},
    {id: 'private', label: 'Private'},
] 

const playlist = reactive({
    name: '',
    description: '',
    visibility: VISIBILITY_OPTIONS[0], // Default to first option.
    owner: 'pip',
    songs: [],
})
const isEditing = ref(false)
const errorMsg = ref(null) // Error message from playlist load request.
const isLoaded = ref(false) // Whether the page has finished loading - either successfully or with an error.
const requestPending = ref(false)

function createPlaylist() {
    requestPending.value = true

    // Should be consistent with the API.
    const playlistData = {
        name: playlist.name,
        description: playlist.description,
        visibility: playlist.visibility,
    }
    PlaylistService.createPlaylist(playlistData).then((data) => {
        Toast.fire({
            title: 'Playlist created',
            icon: 'success',
        })
        router.push('playlists/' + data.id) // Go to the playlists's page
    }).catch((err) => {
        Swal.fire({
            title: 'Error',
            text: 'Failed to create playlist: ' + ((err.response !== undefined) ? err.response.data.detail : err.message),
            icon: 'error',
        })
    }).finally(() => {
        requestPending.value = false
    })
}

function saveChanges() {
    PlaylistService.update({
        id: route.params.id,
        description: playlist.description,
        visibility: playlist.visibility.id,
        songs: playlist.songs,
    }).then(() => {
        Toast.fire({
            title: 'Playlist updated',
            icon: 'success',
        })
        // Only exit edit mode if the request was successful,
        // so the user can quickly retry in case of failure.
        isEditing.value = !isEditing.value
    }).catch((err) => {
        Swal.fire({
            title: 'Error',
            text: 'Failed to save changes: ' + ((err.response !== undefined) ? err.response.data.detail : err.message),
            icon: 'error',
        })
    })
}

// Fetches and assigns playlist data reactive,
// as well as marking the page as loaded and storing error message, if any.
async function fetchPlaylistData(id) {
    try {
        const newData = await PlaylistService.get(id)
        playlist.name = newData.name
        playlist.description = newData.description
        playlist.visibility = VISIBILITY_OPTIONS.find((el) => el.id === newData.visibility)
        playlist.owner = newData.owner
        playlist.songs = newData.songs

        // Clear any previous error message so the new playlist is shown
        errorMsg.value = null
    } catch (err) {
        errorMsg.value = (err.response) ? err.response.data.detail : err.message
    } finally {
        // Mark the page as loaded in either case
        isLoaded.value = true
    }
}

// Refetch playlist data when navigating to another playlist from this page (ex. directly rewriting the URL)
// This is necessary as the component won't be recreated, thus onMounted() won't fire.
watch(
    () => route.params,
    (newId) => {
        fetchPlaylistData(newId)
    }
)

// Fetch playlist data when the page is accessed from another one.
onMounted(function () {
    if (!isCreating()) {
        fetchPlaylistData(route.params.id)
    } else {
        isLoaded.value = true
    }
})

const canEdit = computed(() => {
    return !isCreating() && playlist.owner === UserService.getCurrentUsername()
})

const canCreate = computed(() => {
    return isCreating() && playlist.name !== '' && !requestPending.value // Disallow sending more requests until each has resolved.
})

function isCreating() {
    return route.params.id === 'new'
}

const fullTitle = computed(() => {
    return `${playlist.name} by ${playlist.owner}`
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

.form-container {
    width: 800px;
    box-sizing: border-box; /* Include padding and border in the element's total width and height */
    margin-top: 50px; /* Add some margin to push the form down slightly from the header */
}

.footer-light {
    width: 100vw;
}

.btn-edit {
    @apply font-bold py-3 px-4 rounded;
    @apply bg-blue-500 text-white;
    @apply max-w-min text-nowrap mb-2
}

.btn-edit:hover,
.btn-edit:focus {
    @apply bg-blue-700;
}

.btn-save {
    @apply font-bold py-3 px-4 rounded;
    @apply bg-green-500 text-white;
    @apply max-w-min text-nowrap mb-2
}

.btn-save:hover,
.btn-save:focus {
    @apply bg-green-700;
}

@media (max-width: 768px) {
    .form-container {
        width: 90vw; /* Full viewport width for small screens */
        height: auto; /* Full viewport height for small screens */
        margin-top: 10vh; /* Remove margin for full screen effect */
        border-radius: 0; /* Remove border radius for full screen effect */
    }

}
</style>