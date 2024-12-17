<template>
    <EngagementShape :artist="artist" class="engagement-shape" />
    <div class="artist-container wow fadeInUp" data-wow-duration="600ms" data-wow-delay="300ms">
        <div class="thumb" @mousemove="handleMouseMove">
            <router-link :to="`/users/${artist.username}`" draggable="false">
                <img :src="artist.image" :alt="artist.name" class="clickable-image" />
            </router-link>
            <div class="overlay">
                <h5 class="artist-name">{{ artist.username }}</h5>
                <p class="artist-genre">{{ 				artist.genre
					.split(' ')
					.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
					.join(' ')}}</p>

            </div>
        </div>
    </div>
    <!-- Action Buttons -->
    <div class="action-buttons" v-if="isListener">
        <!-- Follow/Unfollow Button -->
        <button class="action-button follow-button" :class="{ 'is-following': artist.is_following }"
            @click="toggleFollow">
            <i class="fa" :class="artist.is_following ? 'fa-user-minus' : 'fa-user-plus'"></i>
        </button>



        <!-- Message Button (conditionally rendered) -->
        <button v-if="artist.can_ask" class="action-button dialog-button" @click="sendMessage">
            <i class="fa fa-comment"></i>
        </button>
    </div>
</template>

<script>
import EngagementShape from './EngagementShape.vue';
import QuestionService from '../services/question.js';
import UserService from '../services/user.js';
import ListernerService from '../services/listener.js';
import Swal from 'sweetalert2';
import Toast from '../utilities/toast.js';
import { ref, onMounted } from 'vue'; // Include `onMounted` for lifecycle hook
import { useRouter } from 'vue-router';

export default {
    components: {
        EngagementShape,
    },
    name: 'ArtistComponent',
    props: {
        artist: {
            type: Object,
            required: true,
        },
    },
    setup(props, { emit }) {
        const isFollowing = ref(props.artist.is_following);
        const router = useRouter();
        const isListener = ref(false); // Corrected 'False' to 'false'

        // Fetch user data and determine role
        const fetchData = async () => {
            try {
                const user = await UserService.getCurrentUsername(); 
                const role = await UserService.getUserRole(user);

                if (role === 'listener') {
                    isListener.value = true;
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        };

        const toggleFollow = () => {
            isFollowing.value = !isFollowing.value;

            if (isFollowing.value) {
                ListernerService.follow(props.artist.username)
                    .then(() => {
                        Toast.fire({
                            title: `You are now following ${props.artist.username}`,
                            icon: 'success',
                        });
                        emit('edited', { ...props.artist, is_following: true });
                    })
                    .catch((err) => {
                        console.error(err);
                        Toast.fire({
                            title: 'Failed to follow the artist',
                            icon: 'error',
                        });
                        isFollowing.value = false;
                    });
            } else {
                ListernerService.unfollow(props.artist.username)
                    .then(() => {
                        Toast.fire({
                            title: `You have unfollowed ${props.artist.username}`,
                            icon: 'info',
                        });
                        emit('edited', { ...props.artist, is_following: false });
                    })
                    .catch((err) => {
                        console.error(err);
                        Toast.fire({
                            title: 'Failed to unfollow the artist',
                            icon: 'error',
                        });
                        isFollowing.value = true;
                    });
            }
        };

        const sendMessage = () => {
            if (UserService.isLoggedIn() && isFollowing.value) {
                Swal.fire({
                    title: 'Ask me something!',
                    html: `
                        <textarea id="swal-input" class="swal2-textarea" maxlength="500"
                            placeholder="Type your question here..."></textarea>
                    `,
                    showCancelButton: true,
                    confirmButtonText: 'Send',
                    preConfirm: () => {
                        const question = document.getElementById('swal-input').value;
                        if (!question || question.trim().length === 0) {
                            Swal.showValidationMessage('The question cannot be empty');
                            return false;
                        }
                        return question;
                    },
                }).then((result) => {
                    if (result.isConfirmed && result.value) {
                        QuestionService.newQuestion(props.artist.username, result.value)
                            .then(() => {
                                Toast.fire({
                                    title: 'Your question has been sent successfully!',
                                    icon: 'success',
                                });
                                emit('edited', { ...props.artist, can_ask: false });
                            })
                            .catch((err) => {
                                Swal.fire({
                                    title: 'Error',
                                    text: 'Failed to send the question: ' + (err.message || 'Unknown error'),
                                    icon: 'error',
                                });
                            });
                    }
                });
            } else if (!UserService.isLoggedIn()) {
                Toast.fire({
                    title: 'You need to be logged in to send questions to artists',
                    icon: 'warning',
                });
                router.push('/login');
            } else {
                Toast.fire({
                    title: 'You need to follow the artist to send them questions',
                    icon: 'warning',
                });
            }
        };

        const handleMouseMove = (event) => {
            if (!isFollowing.value || event.buttons !== 0) return;

            const body = document.querySelector('body');
            const heart = document.createElement('span');
            heart.classList.add('heart-animation');

            heart.style.left = `${event.clientX + window.scrollX}px`;
            heart.style.top = `${event.clientY + window.scrollY}px`;
            const size = Math.random() * 80;
            heart.style.width = `${20 + size}px`;
            heart.style.height = `${20 + size}px`;

            const transformValue = Math.random() * 360;
            heart.style.transform = `rotate(${transformValue}deg)`;

            body.appendChild(heart);

            setTimeout(() => heart.remove(), 1000);
        };

        // Automatically fetch data when the component is mounted
        onMounted(fetchData);

        return {
            isFollowing,
            toggleFollow,
            sendMessage,
            handleMouseMove,
            fetchData,
        };
    },
};
</script>


<style scoped>
.artist-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
}

.thumb {
    position: relative;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    width: calc(100% - 100px);
    height: calc(100% - 100px);
}

.thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease, opacity 0.3s ease;
    pointer-events: none;
}

.thumb:hover img {
    transform: scale(1.1);
    opacity: 0.8;
}

.overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}

.thumb:hover .overlay {
    opacity: 1;
}

.artist-name,
.artist-genre {
    margin: 0;
    color: white;
}

.artist-name {
    font-size: clamp(1rem, 5%, 2rem);
    /* Dynamically scales with container size */
}

.artist-genre {
    font-size: clamp(0.8rem, 4%, 1.5rem);
    /* Dynamically scales with container size */
    margin-top: 5px;
}

.engagement-shape {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 100;
    pointer-events: none;
}

/* Action Buttons Container */
.action-buttons {
    position: absolute;
    bottom: 20px;
    right: 20px;
    display: flex;
    flex-direction: row;
    /* Align buttons horizontally */
    gap: 10px;
    /* Space between buttons */
}

/* Action Button Styles */
.action-button {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: gray;
    /* Default gray color */
    color: white;
    border: none;
    border-radius: 50%;
    /* Fully rounded button */
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s ease, transform 0.2s ease;
}

/* Follow Button: Blue when following */
.action-button.is-following {
    background-color: #007bff;
    /* Blue color when following */
}

.action-button:hover {
    transform: scale(1.1);
    /* Slightly enlarge on hover */
}

/* Follow Button Hover Animations */
.action-button.follow-button:hover {
    background-color: #0056b3;
    /* Darker blue when hovering (if following) */
}

.action-button.follow-button:not(.is-following):hover {
    background-color: #4caf50;
    /* Green when hovering (if not following) */
}

/* Message Button */
.action-button.dialog-button {
    background-color: #007bff;
    /* Blue color for the message button */
}

.action-button.dialog-button:hover {
    background-color: #0056b3;
    /* Darker blue for the message button */
}

.artist-name {
    font-size: clamp(0.8rem, 1.5vw, 1.2rem);
    /* Minimum size: 0.8rem, scales with viewport width (1.5vw), maximum size: 1.2rem */
    font-weight: bold;
    margin: 0;
    color: white;
}

.artist-genre {
    font-size: clamp(0.6rem, 1vw, 0.9rem);
    /* Minimum size: 0.6rem, scales with viewport width (1vw), maximum size: 0.9rem */
    margin-top: 5px;
    color: white;
}
</style>