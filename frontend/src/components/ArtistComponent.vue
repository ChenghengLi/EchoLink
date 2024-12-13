<template>
    <div class="artist-container wow fadeInUp" data-wow-duration="600ms" data-wow-delay="300ms">
        <div class="thumb" @mousemove="handleMouseMove">
            <router-link :to="`/users/${artist.username}`" draggable="false">
                <img :src="artist.image" :alt="artist.name" class="clickable-image" />
            </router-link>
            <div class="overlay">
                <h5 class="artist-name">{{ artist.username }}</h5>
                <p class="artist-genre">{{ artist.genre }}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ArtistComponent',
    props: {
        artist: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            heartCounter: 0,
        };
    },
    methods: {
        handleMouseMove(event) {
            if (!this.artist.is_following) return; // Check if the artist is followed
            if (event.buttons !== 0) return; // Check if the mouse button is pressed

            this.heartCounter++;
            if (this.heartCounter % 2 !== 0) return;

            let body = document.querySelector('body');
            let heart = document.createElement('span');
            heart.classList.add('heart-animation');

            const x = event.clientX + window.scrollX;
            const y = event.clientY + window.scrollY;
            heart.style.left = x + 'px';
            heart.style.top = y + 'px';

            let size = Math.random() * 80;
            heart.style.width = 20 + size + 'px';
            heart.style.height = 20 + size + 'px';

            let transformValue = Math.random() * 360;
            heart.style.transform = 'rotate(' + transformValue + 'deg)';

            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `
                .heart-animation::before {
                    content: '';
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    background: url(heart.png);
                    background-size: cover;
                    animation: animate 1s linear infinite;
                }
                .heart-animation {
                    z-index: 1000;
                    position: absolute;
                    pointer-events: none;
                    filter: drop-shadow(0 0 15px rgba(0, 0, 0, 0.5));
                }
                @keyframes animate {
                    0% {
                        transform: translate(0) rotate(0deg);
                        opacity: 0;
                    }
                    20%, 80% {
                        opacity: 1;
                    }
                    100% {
                        transform: translate(300px) rotate(360deg);
                        opacity: 0;
                    }
                }
            `;
            document.getElementsByTagName('head')[0].appendChild(style);

            body.appendChild(heart);

            setTimeout(() => {
                heart.remove();
            }, 1000);
        }
    }
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
    font-size: 1.5rem;
}

.artist-genre {
    font-size: 1rem;
    margin-top: 5px;
}
</style>
