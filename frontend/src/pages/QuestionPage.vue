<template>
    <div class="home-two-light question-page home-light container">
      <!-- Header -->
      <HeaderComponent />
  
  
      <!-- Question List Section -->
      <div class="questions-section px-4 mx-auto">
        <h2>Your Questions</h2>
        <p>See how artists have responded to your questions.</p>
  
        <!-- Question List Component -->

        <QuestionList />



      </div>
  
      <!-- Footer -->
      <FooterComponent class="footer-light mx-10" />
    </div>
  </template>
  
  <script setup>
  import HeaderComponent from '../components/HeaderComponent.vue';
  import FooterComponent from '../components/FooterComponent.vue';
  import QuestionList from '../components/QuestionList.vue';
  import UserService from '../services/user.js';
  
  import { reactive, onMounted } from 'vue';
  
  const user = reactive({});
  
  async function fetchUser() {
    try {
      const userData = await UserService.get(UserService.getCurrentUsername());
      Object.assign(user, userData);
    } catch {
      console.error('Failed to load user data');
    }
  }
  
  function getUsername() {
    return UserService.getCurrentUsername();
  }
  
  // Fetch user data when the page is accessed
  onMounted(fetchUser);
  </script>
  
  <style scoped>
  .container {
    width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    min-height: 100vh;
  }
  
  .footer-light {
    width: 100vw;
  }
  
  .banner {
    background-image: url("../assets/images/broadcast-bg.png");
    @apply bg-cover;
  }
  
  .questions-section {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  h2 {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  p {
    font-size: 1rem;
    margin-bottom: 1rem;
  }
  </style>