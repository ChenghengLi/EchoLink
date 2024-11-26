<template>
    <div class="home-two-light home-light container">
        <HeaderComponent />

        <!-- Show a loading spinner while fetching user data -->
        <div v-if="!isLoaded" class="flex">
            <LoadingSpinner class="mx-auto" />
        </div>
        <!-- Profile view -->
        <div v-else-if="isLoaded && errorMsg === null" class="flex flex-col mx-auto max-w-screen-lg w-100">
            <!-- Username, badges and banner area -->
            <div class="banner content-block mx-auto w-100 mt-8 mb-2">
                <!-- Inner banner area -->
                <div class="sm:flex min-h-32 relative">
                    <!-- Avatar and username -->
                    <div class="flex items-end">
                        <img class="max-w-32 min-w-20 h-auto rounded-3 border-black" src="../assets/images/avatar.svg" />
                        
                        <!-- TODO ensure contrast vs banner -->
                        <div class="flex flex-col items-start ms-3">
                            <p class="font-bold text-lg text-white">Welcome back, {{ getUsername() }}</p>
                            <p class="text-md text-white">We've missed your rhythm and creativity!</p>
                        </div>
                    </div>

                    <div class="mx-auto my-3"></div>
                    <!-- Spacing between avatar/username and badges, handles both desktop & mobile layouts -->

                    <div class="absolute right-0 top-0 d-flex flex-column flex-md-row ml-auto mr-md-0">
                        <button class="btn btn-blue max-w-min text-nowrap" @click="router.push('/users/' + getUsername())"
                            data-test="button-edit">
                            <GlobeAltIcon class="icon" />
                            View public profile
                        </button>
                    </div>
                    <!-- Right area; badges & owner controls -->
                    <div class="flex flex-col items-end">

                        <div class="my-auto"></div>
                    </div>
                </div>
            </div>
            <!-- Metrics and activities -->
            <div class="lg:flex">
                <!-- Metrics -->
                <div class="content-block flex flex-grow lg:mr-2">
                    <div class="flex flex-column w-100">
                        <h2 class="section-header">Metrics</h2>
                        <p class="text-left">See how you compare against other artists.</p>

                        <div class="grid grid-cols-2 gap-2">
                            <div v-for="metric in metrics" class="metric flex-col items-center rounded border-2 w-full p-2 border-indigo-200 bg-indigo-300 hover:shadow-lg" v-tooltip="metric.tooltip">
                                <p class="text-lg font-bold">
                                    <!-- Holy fuck, each of these being a separate component is annoying as shit. TODO What's a better way of doing this? -->
                                    <UserIcon v-if="metric.id === 'fans'" class="icon"/>
                                    <PencilIcon v-if="metric.id === 'answer_rate'" class="icon"/>
                                    <StarIcon v-if="metric.id === 'engagement'" class="icon"/>
                                    <TrophyIcon v-if="metric.id === 'ranking'" class="icon"/>
                                    {{ metric.label }}</p>
                                <p>{{ metric.prefix || '' }}{{ metric.value }}{{ metric.suffix || '' }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="my-2"></div> <!-- Used for spacing in column layout (low viewport width) -->

                <!-- Activities -->
                <div class="content-block lg:min-w-80">
                    <h2 class="section-header">Growth</h2>
                    <p>Interact with your fans to boost your growth.</p>

                    <div class="my-3"></div>

                    <!-- TODO setup links -->
                    <div class="flex flex-col items-center">
                        <button class="btn btn-blue w-80 text-nowrap my-1" @click="router.push('/users/' + getUsername())">
                            <GlobeAltIcon class="icon" />
                            View & edit public profile
                        </button>
                        <button class="btn btn-blue w-80 text-nowrap my-1" @click="scrollToQuestions">
                            <QuestionMarkCircleIcon class="icon" />
                            Answer fan questions
                        </button>
                        <!-- <button class="btn btn-blue w-80 text-nowrap my-1" @click="router.push('/users/' + getUsername())">
                            <MegaphoneIcon class="icon" />
                            Send fan acknowledgements
                        </button> -->
                    </div>
                </div>
            </div>

            <!-- Questions -->
            <div class="content-block my-2">
                <h2 class="section-header">Fan Questions</h2>
                <p class="text-left">Answer questions from your fans to boost your engagement.</p>

                <div class="grid lg:grid-cols-2 grid-cols-1 gap-2">
                    <!-- TODO better accessibility -->
                    <div v-for="(question, i) in unansweredQuestions" v-if="unansweredQuestions.length > 0" class="question relative group" @mouseover="hoveredQuestions.add(i)" @mouseleave="hoveredQuestions.delete(i)" @click="answerQuestion(question)" :tabindex="i">
                        <div class="absolute right-2 top-2 d-flex flex-column flex-md-row ml-auto mr-md-0" >
                            <button class="btn btn-blue p-2 max-w-min text-nowrap" :class="{'invisible': !hoveredQuestions.has(i)}"
                                data-test="button-edit">
                                <PencilIcon class="icon" />
                                Answer
                            </button>
                        </div>
                        <div class="flex items-center">
                            <img class="size-8 mr-3" src="../assets/images/avatar.svg"/>
                            <!-- TODO show username? -->
                            <p>A fan asks:</p>
                        </div>
                        <p>{{ question.question_text }}</p>
                    </div>
                    <div v-else>
                        <p class="text-left text-gray-500">You have no unanswered questions.</p>
                    </div>
                </div>
            </div>
        </div>
        <ErrorPanel v-else header="The dashboard could not be loaded:" :reason="errorMsg"></ErrorPanel>

        <FooterComponent class="footer-light" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';
import ErrorPanel from '../components/ErrorPanel.vue';
import UserService from '../services/user.js'
import QuestionService from '../services/questions.js'
import { onMounted, ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { GlobeAltIcon, QuestionMarkCircleIcon, UserIcon, StarIcon, TrophyIcon, PencilIcon } from '@heroicons/vue/24/solid'

const router = useRouter()

// TODO pull from API
const metrics = reactive([
    {id: 'fans', label: 'Fans', tooltip: 'Amount of fans that follow you.', value: 20},
    {id: 'answer_rate', label: 'Answer Rate', tooltip: 'Percentage of questions from fans you\'ve answered.', value: 20, suffix: '%'},
    {id: 'engagement', label: 'Engagement', tooltip: 'How much your fans have interacted with your content. Follows, questions asked and other fan activity all boost your engagement score.', value: 8227},
    {id: 'ranking', label: 'Ranking', tooltip: 'How your Engagement score compares against other EchoLink artists.', value: 22, prefix: 'Top '},
])
const questions = reactive([])
const hoveredQuestions = ref(new Set())
const errorMsg = ref(null) // Error message from profile load request.
const isLoaded = ref(false) // Whether the page has finished loading - either successfully or with an error.

// Profile data. Field names should match the API ones.
const artist = reactive({
    genre: '',
    description: '',
})

function getUsername() {
    return UserService.getCurrentUsername()
}

async function fetchArtistData() {
    try {
        Object.assign(artist, await UserService.get(getUsername()))
        Object.assign(questions, await QuestionService.getUserQuestions())

        // Clear any previous error message so the new profile is shown
        errorMsg.value = null
    } catch (err) {
        errorMsg.value = (err.response) ? err.response.data.detail : err.message
    } finally {
        // Mark the page as loaded in either case
        isLoaded.value = true
    }
}

const unansweredQuestions = computed(() => {
    const unansweredQuestions = questions.filter((question) => question.response_status === 'waiting')
    return unansweredQuestions
})

function answerQuestion(question) {
    alert('TODO')
}

function scrollToQuestions() {
    // TODO change this to use hashes/anchors once we have more elements on the page 
    window.scrollTo(0, document.body.scrollHeight);
}

// Fetch artist data when the page is accessed.
onMounted(function () {
    fetchArtistData()
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

.banner {
    background-image: url("../assets/images/broadcast-bg.png");
    @apply bg-cover
}

.content-block {
    @apply p-4 border-2 rounded-lg border-indigo-100 bg-indigo-200
}

.section-header {
    @apply text-left font-bold text-xl mb-2
}

.btn {
    @apply font-bold py-3 px-4 rounded;
}

.btn-blue {
    @apply bg-blue-500 text-white;
}

.btn-blue:hover,
.btn-blue:focus {
    @apply bg-blue-700;
}

.btn-red {
    @apply bg-red-500 text-white;
}

.btn-red:hover,
.btn-red:focus {
    @apply bg-red-700;
}

.container {
    width: 100vw;
}

.banner {
    background-image: url("../assets/images/broadcast-bg.png");
    @apply bg-cover
}

.metric {
    @apply text-white
}

.question {
    @apply rounded border-2 w-full p-3 border-indigo-200 bg-indigo-300 shadow-lg cursor-pointer
}

@media (max-width: 900px) {
    .container-main {
        width: 90%; /* Full viewport width for small screens */
        height: auto; /* Full viewport height for small screens */
        margin-top: 10vh; /* Remove margin for full screen effect */
        border-radius: 0; /* Remove border radius for full screen effect */
    }
}

</style>