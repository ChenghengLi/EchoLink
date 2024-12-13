<template>
    <section class="section artists pb-0 pt-3">
        <div class="container">
            <!-- Header -->
            <div v-if="showHeader" class="row justify-content-center">
                <div class="col-12 col-xl-8">
                    <div data-wow-duration="600ms" data-wow-delay="300ms" class="section__header wow fadeInUp">
                        <h2 ref="artistsHeader" class="h2">Artists</h2>
                    </div>
                </div>
            </div>

            <!-- Artist Carousel -->
            <div class="artist-carousel mt-4">
                <Flicking ref="carousel" :options="{ gap: 30, align: 'center' }" class="carousel-with-blur">
                    <div v-for="artist in artists" :key="artist.username" class="artist-card">
                        <ArtistComponent :artist="artist" />
                    </div>
                    <div v-if="artists.length != 0" class="artist-card view-all-artists-div">
                        <h4>Want to see a list of your favorite artists?</h4>
                        <button @click="$router.push('/artist')" class="btn btn--primary mt-3 min-w-64 text-black">Click here!</button>
                    </div>
                </Flicking>
            </div>
        </div>
    </section>
</template>

<script>
import { defineComponent } from 'vue';
import Flicking from '@egjs/vue3-flicking';
import '@egjs/vue3-flicking/dist/flicking.css';
import ArtistComponent from './ArtistComponent.vue';
import ListenerService from '../services/listener.js';
import fixedImage from '../assets/images/cara1.jpg';

export default defineComponent({
    components: {
        Flicking,
        ArtistComponent,
    },
    data() {
        return {
            artists: []
        };
    },
    methods: {
        async fetchArtists() {
            try {
                const data = await ListenerService.getPreferences();
                this.artists = data.map((artist) => ({
                    ...artist,
                    image: artist.image_url || fixedImage,
                }));
            } catch (error) {
                console.error('Error fetching artists:', error);
            }
        }
    },
    props: {
        showHeader: Boolean,
    },
    created() {
        this.fetchArtists();
    },
});
</script>

<style scoped>
.artist-card {
    position: relative;
    height: 400px;
    width: 400px;
    margin: 0 30px;
}

.carousel-with-blur {
    position: relative;
    max-width: 1000px;
    margin: 0 auto;
    -webkit-mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-size: 100% 100%;
    mask-size: 100% 100%;
}

.flicking-viewport {
    overflow: visible;
}

.flicking-camera {
    display: flex;
    gap: 30px;
}

.artist-carousel {
    margin-top: 20px;
    padding: 10px;
    max-width: 1000px;
    margin-left: auto;
    margin-right: auto;
}

.view-all-artists-div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

</style>
