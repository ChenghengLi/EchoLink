<template>
	<div>
		<div class="home-two-light my-app home-light container">

			<Header />
			<Banner />
			<Broadcast />
			<ArtistsList />
			<Footer class="footer-light mx-10" />
		</div>
		<div class="progress-wrap active-progress" @click="scrollToTop">
			<svg width="100%" height="100%" viewBox="-1 -1 102 102" class="progress-circle svg-content">
				<path d="M50,1 a49,49 0 0,1 0,98 a49,49 0 0,1 0,-98" style="transition: stroke-dashoffset 10ms linear; stroke-dasharray: 307.919, 307.919; stroke-dashoffset: 178,377;"></path>
			</svg>
		</div>

	</div>
</template>

<script>
import Header from '../components/HeaderComponent.vue';
import Footer from '../components/FooterComponent.vue';
import Banner from '../components/BannerComponent.vue';
import Broadcast from '../components/BroadcastComponent.vue';
import ArtistsList from '../components/ArtistsList.vue';
export default {
	name: "HomeLight",
	components: {
		Header,
		Footer,
		Banner,
		Broadcast,
		ArtistsList,

	}, mounted(){
		const progressPath = this.$el.querySelector(".progress-wrap path");
  		const pathLength = 307.919;

		const updateProgress = () => {
			const scrollTop = window.scrollY;
			const docHeight = document.documentElement.scrollHeight - window.innerHeight;
			const progress = (scrollTop / docHeight) * 100;

			const offset = pathLength - (pathLength * progress) / 100;
			progressPath.style.strokeDashoffset = offset;
		};

		window.addEventListener("scroll", updateProgress);
		updateProgress();
	}, beforeDestroy(){
		window.removeEventListener("scroll", this.updateProgress);
	}, methods: {
		scrollToBroadcast() {
			this.$nextTick(() => {
				this.$refs.broadcastComponent.$el.scrollIntoView({ behavior: 'smooth' });
			});
		},
		scrollToTop(){
			window.scrollTo({ top: 0, behavior: 'smooth' });
		}
	}
};
</script>

<style scoped>
.home-two-dark .anime--light {
	display: none;
}

.container {
    width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align items to the top */
}


.home-two-light .anime--dark {
	display: none;
}
</style>
