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
                <div class="flex min-h-32">
                    <!-- Avatar and username -->
                    <div class="flex items-end">
                        <img class="max-w-100 min-w-20 h-auto rounded-3 border-black" src="../assets/images/placeholder.png" />
                        <!-- TODO ensure contrast vs banner -->
                        <p class="ms-3 font-bold text-lg text-white">{{ route.params.username }}</p>
                    </div>

                    <div class="mx-auto"></div>

                    <!-- Right area; badges & owner controls -->
                    <div v-if="isOwnProfile" class="flex flex-col items-end">
                        <button class="btn btn-blue max-w-min text-nowrap"><PencilIcon class="icon"/> Edit Profile</button>

                        <div class="my-auto"></div>

                        <!-- Badges area -->
                        <div class="flex">
                            <!-- TODO modify this once we have other user roles -->
                            <div class="badge bg-indigo-500">
                                <span class="text-white"><MusicalNoteIcon class="icon"/> Music Fan</span>
                            </div>
                            <div class="badge bg-blue-500" v-if="isOwnProfile"> <!-- Redundant to show this for other users; if their profile is accessible, then it means it's already public (or from a friend user) -->
                                <span class="text-white"><GlobeAltIcon class="icon"/> Public Profile</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Description and details -->
            <div class="flex">
                <!-- Description -->
                <div class="content-block flex flex-grow mr-2">
                    <div>
                        <h2 class="section-header">About</h2>
                        <p class="text-left">{{ user.description }}</p>
                    </div>
                </div>
                <!-- Details -->
                <!-- TODO make this wrap on lower res -->
                <div class="content-block min-w-80">
                    <h2 class="section-header">Details</h2>
                    <div class="flex">
                        <p><span><MusicalNoteIcon class="icon"/> Favorite Genre:</span></p>
                        <div class="mx-auto"></div>
                        <p>{{ user.genre }}</p>
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
import { computed, onMounted, ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { PencilIcon, MusicalNoteIcon, GlobeAltIcon } from '@heroicons/vue/24/solid'

const router = useRouter()
const route = useRoute()

const errorMsg = ref(null)
const user = ref(null)

async function fetchUserData() {
    try {
        user.value = await UserService.get(route.params.username)
    } catch (err) {
        errorMsg.value = err.message
    }
}

const isLoaded = computed(() => {
    return user !== null || errored.value
})

const isOwnProfile = computed(() => {
    return UserService.isLoggedIn()
})

// Refetch user data when navigating to another profile
// This is necessary as the component won't be recreated.
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
.btn-blue:hover {
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
</style>