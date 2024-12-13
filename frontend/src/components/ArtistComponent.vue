<template>
    <div class="artist-container wow fadeInUp" data-wow-duration="600ms" data-wow-delay="300ms">
        <div class="thumb">
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
