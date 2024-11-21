<template>
    <div class="home-two-light home-light container">

        <HeaderComponent />
        <!-- Set a fixed width for the container -->
        <div class="form-container mx-auto p-4 mt-8 border-3 rounded-lg border-indigo-100 bg-indigo-200">
            <div class="mb-3">
                <h2>Create Playlist</h2>
            </div>

            <!-- Form field container -->
            <div class="px-4 mx-auto">
                <!-- Playlist name -->
                <TextInput label="Playlist Name" :required="true" placeholder="My playlist" input-type="text" :value="playlist.name" @changed="playlist.name = $event"></TextInput>
                <!-- Description -->
                <TextInput label="Description" placeholder="Describe your playlist..." input-type="text" :value="playlist.name" @changed="playlist.description = $event" :multiline="true" :max-length="DESCRIPTION_MAX_LENGTH"></TextInput>

                <!-- Visibility -->
                <Selector v-model="playlist.visibility" :options="VISIBILITY_OPTIONS" label="Visibility" track-by="id" option-label-key="label" :allow-empty="false" :can-search="false"></Selector>
            </div>

            <button class="btn btn--primary w-100 w-md-60 mt-3" :disabled="!canCreate" @click="createPlaylist">Create</button>
        </div>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import Selector from '../components/form/Selector.vue';
import Swal from 'sweetalert2'
import { computed, reactive } from 'vue';
import { useRouter } from 'vue-router';

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
})

function createPlaylist(){
    alert('TODO')
}

const canCreate = computed(() => {
    return playlist.name !== ''
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
    width: 600px;
    box-sizing: border-box; /* Include padding and border in the element's total width and height */
    margin-top: 50px; /* Add some margin to push the form down slightly from the header */
}

.footer-light {
    width: 100vw;
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