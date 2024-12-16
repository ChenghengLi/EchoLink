<template>
	<div>
		<div class="home-two-light my-app home-light page-container">

			<HeaderComponent />

			<div class="lg:px-4 mx-auto max-w-screen-xl">
				<h2>Explore Artists</h2>
				<p>See if your artists answered you.</p>

				<!-- Search and filters -->
				<TextInput class="w-full lg:w-4/4" placeholder="Search by Artist or Content..."
					input-type="text" :value="search.text" @changed="search.text = $event"></TextInput>

				<div class="mx-2 my-2" /> <!-- Spacing -->

				<div class="flex justify-center gap-4 my-4">
					<div class="content-block max-h-min max-w-lg lg:min-w-96 flex-grow">
						<OptionSelector v-model="search.genre" :options="genres" label="Filter by Genre" track-by="id"
							option-label-key="label" :allow-empty="false" :can-search="true"></OptionSelector>
					</div>

					<div class="content-block max-h-min max-w-lg lg:min-w-96 flex-grow">
						<OptionSelector v-model="search.order" :options="orders" label="Sort by" track-by="id"
							option-label-key="label" :allow-empty="false" :can-search="true"></OptionSelector>
					</div>
				</div>

				<div class="mx-2 my-2" /> <!-- Spacing -->

				<div v-if="!sortedArtistsError && sortedArtists.length > 0" class="flex-col items-center mt-3 gap-4">
					<div class=" lg:flex-row items-center justify-center gap-4" >

						<!-- Artist Grid -->
						<div class="artist-grid mt-4">
							<div v-for="artist in filterArtists()" :key="artist.username" class="artist-card">
								<ArtistComponent :artist="artist" />
							</div>

						</div>
					</div>
				</div>


				<p v-else-if="sortedArtistsError" class="text-gray-500">Something went wrong while fetching latest
					artists:
{{ sortedArtistsError }}.
Try refreshing the page.</p>
				<p v-else-if="sortedArtists.length == 0" class="text-gray-500">There are no artists registered on the
					platform.</p>

				<p v-else class="text-gray-500">Something went wrong while fetching the artists :
{{
					sortedArtistsError
				}}.
Try refreshing the page.</p>
			</div>

			<FooterComponent class="footer-light mx-10" />
		</div>
		<div class="progress-wrap active-progress" @click="scrollToTop">
			<svg width="100%" height="100%" viewBox="-1 -1 102 102" class="progress-circle svg-content">
				<path d="M50,1 a49,49 0 0,1 0,98 a49,49 0 0,1 0,-98"
					style="transition: stroke-dashoffset 10ms linear; stroke-dasharray: 307.919, 307.919; stroke-dashoffset: 178,377;">
				</path>
			</svg>
		</div>

	</div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import OptionSelector from '../components/form/OptionSelector.vue';
import ArtistComponent from '../components/ArtistComponent.vue';
import ArtistService from '../services/artist.js'; // Assume this service handles API calls
import { reactive, ref, computed, onMounted, onBeforeUnmount, watch, onUpdated } from 'vue';
import fixedImage from '../assets/images/cara1.jpg';
const genres = reactive([{ id: 'all', label: 'All' }])
const registeredGenres = ref(new Set())


const search = reactive({
	genre: { id: 'all', label: 'All' },
	text: '',
	order: { id: 0, label: 'Engagment'  },
})


let fetchedArtists = []
const sortedArtists = reactive([])
const sortedArtistsError = ref(null)
const orders = reactive([
	{ id: 2, label: 'Alphabetically' },
	{ id: 1, label: 'Followers' },
	{ id: 0, label: 'Engagment' },

]);



function filterArtists() {
	let filtered = [...sortedArtists]

	// Filter by genre
	if (search.genre.id !== 'all') {
		filtered = filtered.filter(artist => artist.genre === search.genre.id)
	}

	// Apply search text filter
	if (search.text.trim() !== '') {
		const searchText = search.text.toLowerCase()
		filtered = filtered.filter(artist =>
			artist.username.toLowerCase().includes(searchText) ||
			artist.genre.toLowerCase().includes(searchText) // Search in artist name or content
		)
	}

	// Sort the filtered artists based on the selected order
	if (search.order.id === 2) {
		// Alphabetically
		filtered.sort((a, b) => a.username.localeCompare(b.username))
	}else if (search.order.id === 0) {
		// By Engagement
		filtered.sort((a, b) => a.rank_data.ranking - b.rank_data.ranking)
	} 


	return filtered
	
}


async function fetchArtists() {
	try {
		fetchedArtists = await ArtistService.getArtistByFollowers() 
		fetchedArtists = fetchedArtists.map((artist) => ({
			...artist,
			image: artist.image_url || fixedImage,
		}));

		// Track all used genres
		for (const index in fetchedArtists) {
			const artist = fetchedArtists[index]

			if (!registeredGenres.value.has(artist.genre)) {
				genres.push({ id: artist.genre, label: artist.genre })
				registeredGenres.value.add(artist.genre)
			}
		}

		if (!genres.some(genre => genre.id === 'all')) {
			genres.unshift({ id: 'all', label: 'All' });
		}

		Object.assign(sortedArtists, fetchedArtists)


	} catch (err) {
		sortedArtistsError.value = (err.response) ? err.response.data.detail : err.message
	}
}

onUpdated(() => {
	updateProgress() // Must update the scroll widget as the page dimensions most likely changed, ex. if artists were fetched.
})

function scrollToTop() {
	window.scrollTo({ top: 0, behavior: 'smooth' });
}



const updateProgress = () => {
	const progressPath = document.querySelector(".progress-wrap path");
	const pathLength = 307.919;
	const scrollTop = window.scrollY;
	const docHeight = document.documentElement.scrollHeight - window.innerHeight;
	const progress = (scrollTop / docHeight) * 100;

	const offset = pathLength - (pathLength * progress) / 100;
	progressPath.style.strokeDashoffset = offset;
};

onMounted(() => {
	fetchArtists();

	window.addEventListener("scroll", updateProgress);
	updateProgress();
})

onBeforeUnmount(() => {
	window.removeEventListener("scroll", updateProgress);
});

</script>

<style scoped>
.home-two-dark .anime--light {
	display: none;
}

.page-container {
	width: 100vw;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: flex-start;
	/* Align items to the top */
}


.home-two-light .anime--dark {
	display: none;
}

.artist-grid {
	display: grid;
	grid-template-columns: 1fr;
	/* Default to 1 column */
	gap: 30px;
	max-width: 1000px;
	margin: 0 auto;
	padding: 10px;
}

@media (min-width: 768px) {
	.artist-grid {
		grid-template-columns: repeat(2, 1fr);
		/* 2 columns for medium screens */
	}
}

@media (min-width: 1200px) {
	.artist-grid {
		grid-template-columns: repeat(3, 1fr);
		/* 3 columns for large screens */
	}
}


.artist-card {
	position: relative;
	width: 100%;
	/* Adjust width to fit grid column */
	padding-top: 100%;
	/* This ensures the card is square by making height proportional to width */
	background-color: #f9f9f9;
	/* Optional: Add a background color */
	overflow: hidden;
	
}

.artist-card>* {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
}

.view-all-artists-div {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.artist-card {
	position: relative;
	width: 100%;
	padding-top: 100%; /* Ensures the card is square */
	background-color: #f9f9f9;
	overflow: hidden;
	z-index: 1; /* Ensure it has a lower z-index */
}

.artist-card > * {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	z-index: 1; /* Ensure child elements also have a lower z-index */
}

.artist-grid {
	display: grid;
	grid-template-columns: 1fr; /* Default to 1 column */
	gap: 30px;
	max-width: 1000px;
	margin: 0 auto;
	padding: 10px;
	z-index: 1; /* Ensure the grid itself has a lower z-index */
}

@media (min-width: 768px) {
	.artist-grid {
		grid-template-columns: repeat(2, 1fr); /* 2 columns for medium screens */
	}
}

@media (min-width: 1200px) {
	.artist-grid {
		grid-template-columns: repeat(3, 1fr); /* 3 columns for large screens */
	}
}

/* Ensure the header and selectors have a higher z-index */
.home-two-light .my-app {
	position: relative;
	z-index: 10; /* Higher z-index for the header and selectors */
}

.header-component,
.option-selector {
	position: relative;
	z-index: 10; /* Ensure these components are above the artist grid */
}
</style>
