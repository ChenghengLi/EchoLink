<template>
    <div class="home-two-light home-light container">
        <HeaderComponent />

        <!-- Show a loading spinner while fetching user data -->
        <div v-if="!isLoaded" role="status">
            <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
            </svg>
            <span class="sr-only">Loading...</span>
        </div>
        <div v-else-if="user" class="flex flex-col mx-auto max-w-screen-lg">
            <!-- Username, badges and banner area -->
            <div class="banner content-block mx-auto w-100 mt-8 mb-2">
                <!-- Inner banner area -->
                <div class="sm:flex min-h-32 relative">
                    <!-- Avatar and username -->
                    <div class="flex items-end">
                        <img class="max-w-100 min-w-20 h-auto rounded-3 border-black" src="../assets/images/placeholder.png" />
                        <!-- TODO ensure contrast vs banner -->
                        <p class="ms-3 font-bold text-lg text-white">{{ route.params.username }}</p>
                    </div>

                    <div class="mx-auto my-3"></div> <!-- Spacing between avatar/username and badges, handles both desktop & mobile layouts -->
                    
                    <!-- "Edit Profile" button; always in top-right -->
                    <div class="absolute right-0 top-0">
                        <button v-if="isOwnProfile" class="btn btn-blue max-w-min text-nowrap" @click="toggleEditMode">
                            <PencilIcon class="icon"/>
                            {{ isEditing ? "Save Changes" : "Edit Profile" }}
                        </button>
                    </div>

                    <!-- Right area; badges & owner controls -->
                    <div class="flex flex-col items-end">

                        <div class="my-auto"></div>

                        <!-- Badges area -->
                        <div class="flex">
                            <!-- TODO modify this once we have other user roles -->
                            <div class="badge bg-indigo-500">
                                <span class="text-white"><MusicalNoteIcon class="icon"/> Music Fan</span>
                            </div>
                            <div v-if="isOwnProfile" :class="visibilityBadgeClass" class="badge bg-blue-500" @click="user.visibility = !user.visibility"> <!-- Redundant to show this for other users; if their profile is accessible, then it means it's already public (or from a friend user) -->
                                <span class="text-white">
                                    <span v-if="!isEditing" class="text-white">
                                        <GlobeAltIcon class="icon"/>
                                         {{ user.visibility ? "Public Profile" : "Private Profile" }}
                                    </span>
                                    <!-- When editing, show a checkbox instead of the globe icon -->
                                    <span v-else class="flex max-w-fit items-center text-white">
                                        <input class="size-4 mr-1" type="checkbox" v-model="user.visibility"/>
                                        <!-- When editing, always show this badge as "Public Profile" to clarify the meaning of on/off for the checkbox. -->
                                         Public Profile
                                    </span>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Description and details -->
            <div class="lg:flex">
                <!-- Description -->
                <div class="content-block flex flex-grow lg:mr-2">
                    <div class="flex flex-column">
                        <h2 class="section-header">About</h2>
                        <textarea cols="999999" autocomplete="off" autocorrect="on" :class="editableFieldClass" class="details-field text-left flex-grow w-100 min-w-full min-h-60" :maxlength="DESCRIPTION_MAX_LENGTH" placeholder="Describe yourself" :readonly="!isEditing" v-model="user.description"></textarea>
                    </div>
                </div>

                <div class="my-2"></div> <!-- Used for spacing in column layout (low viewport width) -->

                <!-- Details -->
                <!-- TODO make this wrap on lower res -->
                <div class="content-block min-w-96">
                    <h2 class="section-header">Details</h2>
                    <div class="flex">
                        <p><span class="text-nowrap mr-2"><MusicalNoteIcon class="icon"/> Favorite Genre:</span></p>
                        <div class="mx-auto"></div>
                        <input type="text" :maxlength="GENRE_MAX_LENGTH" :class="editableFieldClass" class="details-field text-right max-w-min" placeholder="Favorite genre" list="genresList" :readonly="!isEditing" v-model="user.genre"></input>
                        <datalist id="genresList">
                            <option v-for="genre in genres" :value="genre"/>
                        </datalist>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="content-block max-w-sm mx-auto">
            <p>The profile could not be loaded:</p>
            <p>{{ errorMsg }}</p>
            <RouterLink to="/">Return to homepage</RouterLink>
        </div>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import UserService from '../services/user.js'
import Swal from 'sweetalert2'
import Toast from '../utilities/toast.js'
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { PencilIcon, MusicalNoteIcon, GlobeAltIcon } from '@heroicons/vue/24/solid'
import { reactive } from 'vue';

const route = useRoute()

// Max lengths of fields, in characters.
// TODO adjust these to match backend
const DESCRIPTION_MAX_LENGTH = 120
const GENRE_MAX_LENGTH = 20

// TODO ideally this would be fetched from a DB to make it easier to maintain.
const genres = ["Rock", "Pop"]

const errorMsg = ref(null)
const isEditing = ref(false)
const loaded = ref(false)
const user = reactive({
    genre: '',
    description: '',
    visibility: true,
})

// Fetches and assigns user data reactive,
// as well as marking the page as loaded and storing error message, if any.
async function fetchUserData() {
    try {
        Object.assign(user, await UserService.get(route.params.username))
    } catch (err) {
        errorMsg.value = err.message
    } finally {
        loaded.value = true
    }
}

function toggleEditMode() {
    // Post to save changes
    if (isEditing.value) {
        UserService.updateProfile(user).then(() => {
            Toast.fire({
                title: 'Profile updated',
                icon: 'success',
            })
            // Only exit edit mode if the request was successful,
            // so the user can quickly retry in case of failure.
            isEditing.value = !isEditing.value
        }).catch((err) => {
            Swal.fire({
                title: 'Error',
                text: 'Failed to save changes:' + err.message, 
                icon: 'error',
            })
        })
    } else {
        // Enter edit mode immediately
        isEditing.value = !isEditing.value
    }
}

const isLoaded = computed(() => {
    return loaded.value
})

const isOwnProfile = computed(() => {
    return UserService.isLoggedIn()
})

const editableFieldClass = computed(() => {
    return {
        "details-field-editable": isEditing.value,
    }
})

// Make the badge behave like a button when in edit mode,
// as clicking it will also interact with the checkbox.
const visibilityBadgeClass = computed(() => {
    return {
        "hover:bg-blue-600": isEditing.value,
        "focus:bg-blue-600": isEditing.value,
        "active:bg-blue-500": isEditing.value,
    }
})

// Refetch user data when navigating to another profile from this page (ex. directly rewriting the URL)
// This is necessary as the component won't be recreated, thus onMounted() won't fire.
watch(
    () => route.params.id,
    (newId, _) => {
        fetchUserData(newId)
    }
)

// Fetch user data when the page is accessed from another one.
onMounted(function () {
    fetchUserData(route.params.username)
})

</script>

<style scoped>
.btn {
    @apply font-bold py-3 px-4 rounded;
}
.btn-blue {
    @apply bg-blue-500 text-white;
}
.btn-blue:hover, .btn-blue:focus {
    @apply bg-blue-700;
}
.icon {
    @apply h-4 inline
}
.badge {
    @apply max-h-max mx-1 rounded-md select-none text-white
}
.container{
    width: 100vw;
}
.banner {
    background-image: url("../assets/images/broadcast-bg.png");
    @apply bg-cover
}
.content-block {
    @apply p-4 border-2 rounded-lg border-indigo-100 bg-indigo-200
}
.section-header {
    @apply text-left font-bold text-xl
}

.details-field {
    /* Padding is used for nicer spacing to the input field boundaries; it's declared in this field as well to prevent the text from changing position when toggling edit mode. */
    @apply px-2 bg-transparent max-h-min
}
.details-field::placeholder {
    @apply text-gray-400
}

.details-field-editable {
    @apply bg-gray-50 border border-gray-300 rounded-lg
}

</style>