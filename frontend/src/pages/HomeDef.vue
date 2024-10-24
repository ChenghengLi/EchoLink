<template>
	<div>
		<div class="home-two-light my-app home-light">

			<Header/>
			<Banner />
			<Broadcast />
			<Footer class="footer-light mx-10" />
		</div>

	</div>
</template>

<script>
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
import Banner from '../components/Banner.vue';
import Broadcast from '../components/Broadcast.vue';
export default {
	name: "HomeLight",
	components: {
		Header,
		Footer,
		Banner,
		Broadcast,

	}, methods: {
		scrollToBroadcast() {
        this.$nextTick(() => {
            this.$refs.broadcastComponent.$el.scrollIntoView({ behavior: 'smooth' });
        });
    }
	}
};
</script>

<style>
.home-two-dark .anime--light {
	display: none;
}

.home-two-light .anime--dark {
	display: none;
}
</style>
