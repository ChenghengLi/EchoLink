<template>
    <div class="home-two-light home-light container">

        <HeaderComponent />
        <!-- Set a fixed width for the container -->
        <div class="form-container mx-auto p-4 mt-8 border-3 rounded-lg border-indigo-100 bg-indigo-200">
            <div class="mb-3">
                <h2>Upload a new track</h2>
            </div>

            <!-- Form field container -->
            <div class="px-4 mx-auto">
                <!-- Basic info -->
                <TextInput label="Title" :required="true" placeholder="Title" input-type="text" :value="songtitle" @changed="songtitle = $event" :warning="titleWarning" :test-id="'field-title'"></TextInput>
                <TextInput label="Genre" :required="true" placeholder="Genre" input-type="text" :value="genre" @changed="genre = $event" :warning="genreWarning" :test-id="'field-genre'"></TextInput>
                <TextInput label="Link" :required="true" placeholder="Link" input-type="text" :value="link" @changed="link = $event" :warning="linkWarning" :test-id="'field-link'"></TextInput>
                <hr class="h-divider"/>

                <button class="btn btn--primary w-100 w-md-60" :disabled="!canUpload" @click="uploadTrack" :data-test="'button-uploadTrack'">Upload Track</button>

            </div>
        </div>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import UserService from '../services/user.js'
import Swal from 'sweetalert2'
import Toast from '../utilities/toast.js'
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const songtitle = ref('')
const genre = ref('')
const link = ref('')

function uploadTrack() {
    // Ara està fent la crida a registerAccount perque es d'on he pillat el codi, quan estigui el backend fet per pujar cançons canviar-ho
    UserService.registerAccount(username.value, email.value, password.value).then(() => {
        Toast.fire({
            title: 'Track uploaded successfully!',
            icon: 'success',
        })
        router.push('/')
    }).catch((err) => {
        Swal.fire({
            title: 'Track upload failed',
            text: (err.response !== null) ? err.response.data.detail : err.message,
            icon: 'error',
        })
    })
}
const isTitleValid = computed(() => {
    return (songtitle.value !== '')
})
const isGenreValid = computed(() => {
    return (genre.value !== '')
})
const isLinkValid = computed(() => {
    return (link.value !== '')
})
const canUpload = computed(() => {
    return isTitleValid.value && isGenreValid.value && isLinkValid.value
})

// Warnings for invalid fields
const titleWarning = computed(() => {
    if (songtitle.value === '') {
        return 'This field is required';
    }
})
const genreWarning = computed(() => {
    if (genre.value === '') {
        return 'This field is required';
    }
})
const linkWarning = computed(() => {
    if (link.value === '') {
        return 'This field is required';
    }
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