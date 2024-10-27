<template>
	<header :class="{ 'header-active': scrollPosition >= 100, }" class="header">
		<div class="container">
			<div class="row">
				<div class="col-lg-12">
					<nav class="nav">
						<div class="nav__content">
							<div class="nav__logo">
								<router-link to="/">
									<img :src="LogoURL" alt="Logo" />
								</router-link>
							</div>
							<div class="nav__menu">
								<div class="nav__menu-logo d-flex d-xl-none">
									<router-link to="/" class="text-center hide-nav">
										<img :src="LogoURL" alt="Logo"/>
									</router-link>
									<button aria-label="close the menu" class="nav__menu-close">
										<i class="fa-solid fa-xmark"></i>
									</button>
								</div>
								<ul class="nav__menu-items">
									<!-- De moment, això no es necessita
									<li class="nav__menu-item">
										<router-link to="/" class="nav__menu-link hide-nav">Home</router-link>
									</li>
									<li class="nav__menu-item">
										<router-link to="/about" class="nav__menu-link hide-nav">About
											Us</router-link>
									</li>
									<li class="nav__menu-item">
										<router-link to="/resources"
											class="nav__menu-link hide-nav">Resources</router-link>
									</li>
									<li class="nav__menu-item nav__menu-item--dropdown">
										<a href="javascript:void(0)" class="nav__menu-link nav__menu-link--dropdown">
											Activities
										</a>
										<ul class="nav__dropdown">
											<li>
												<router-link to="/"
													class="nav__dropdown-item hide-nav">Upcoming</router-link>
											</li>
										</ul>
									</li>
									-->

									<li v-if="!isLoggedIn" class="nav__menu-item d-block d-md-none">
										<router-link to="/logIn" class="btn btn--secondary mb-4">
											Log In
										</router-link>
										<router-link to="/register" class="btn btn--secondary">
											Sign In
										</router-link>
									</li>
									<li v-else class="nav__menu-item d-block d-md-none">
										<router-link to="/" class="btn btn--secondary">
											Log Out
										</router-link>
									</li>
								</ul>
							</div>
							<div class="nav__uncollapsed">
								<div class="nav__uncollapsed-item d-none d-md-flex">
									<router-link v-if="!isLoggedIn" to="/logIn" class="btn btn--secondary">
										Log In
									</router-link>
									<router-link v-if="!isLoggedIn" to="/register" class="btn btn--secondary">
										Sign In
									</router-link>
									<router-link v-else to="/" class="btn btn--secondary">
										Log Out
									</router-link>
								</div>
								<button class="nav__bar d-block d-xl-none">
									<span class="icon-bar top-bar"></span>
									<span class="icon-bar middle-bar"></span>
									<span class="icon-bar bottom-bar"></span>
								</button>
							</div>
						</div>
					</nav>
				</div>
			</div>
		</div>
		<div class="backdrop"></div>
	</header>
</template>

<script>

import logo from '../assets/logo.png';

export default {
	name: "HeaderComponent",
	data: function () {
		return {
			scrollPosition: null,
			LogoSrc : logo
		};
	},
	methods: {
		updateScroll() {
			this.scrollPosition =
				window.scrollY;
		},
	},
	mounted() {
		// Router won't exist in tests
		if (this.$router) {
			this.$router.beforeEach((to, from, next) => {
				window.scrollTo(0, 0);
				next();
			});
		}

		const navBars = document.querySelectorAll('.nav__bar');
		const navMenus = document.querySelectorAll('.nav__menu');
		const backdrops = document.querySelectorAll('.backdrop');
		const navDropdowns = document.querySelectorAll('.nav__dropdown');
		const navDropdownLinks = document.querySelectorAll('.nav__menu-link--dropdown');
		const navMenuClose = document.querySelectorAll('.nav__menu-close');
		const ticketModals = document.querySelectorAll('.ticket-modal');
		const conferenceModals = document.querySelectorAll('.conference-modal');
		const body = document.body;

		function toggleMenuActive() {
			navBars.forEach(navBar =>
				navBar.classList.toggle('nav__bar-toggle')
			);

			navMenus.forEach(navMenu =>
				navMenu.classList.toggle('nav__menu-active')
			);

			backdrops.forEach(backdrop =>
				backdrop.classList.toggle('backdrop-active')
			);

			//body.classList.toggle('body-active');
		}

		navBars.forEach(navBar => {
			navBar.addEventListener('click', function () {
				toggleMenuActive();
			});
		});

		backdrops.forEach(backdrop => {
			backdrop.addEventListener('click', function () {
				toggleMenuActive();
			});
		});

		navMenuClose.forEach(menuClose => {
			menuClose.addEventListener('click', function () {
				toggleMenuActive();
			});
		});

		window.addEventListener('resize', function () {
			backdrops.forEach(backdrop =>
				backdrop.classList.remove('backdrop-active')
			);

			navBars.forEach(navBar =>
				navBar.classList.remove('nav__bar-toggle')
			);

			navMenus.forEach(navMenu =>
				navMenu.classList.remove('nav__menu-active')
			);

			navDropdowns.forEach(navDropdown =>
				navDropdown.classList.remove('nav__dropdown-active')
			);

			navDropdownLinks.forEach(navDropdownLink =>
				navDropdownLink.classList.remove('nav__menu-link--dropdown-active')
			);

			body.classList.remove('body-active');

			ticketModals.forEach(ticketModal =>
				ticketModal.style.display = 'none'
			);

			conferenceModals.forEach(conferenceModal =>
				conferenceModal.style.display = 'none'
			);
		});

		navDropdownLinks.forEach(dropdownLink => {
			dropdownLink.addEventListener('click', function () {
				const dropdown = this.nextElementSibling;
				dropdown.classList.toggle('nav__dropdown-active');
				this.classList.toggle('nav__menu-link--dropdown-active');
			});
		});

	},
	props: {
		LogoSrc: {
			type: String,
			required: true,
		},
		isLoggedIn: {
			type: Boolean,
			default: false,
		},
	},
	computed: {
		LogoURL() {
			return this.LogoSrc; 
		},

		SessioIniciada(){
			return true;
		},
	},
};
</script>