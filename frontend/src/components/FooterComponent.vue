<template>
  <footer class="footer-two section bg-img">
    <div class="container">
      <div class="row items-gap-two justify-content-between align-items-center">
        <div class="col-auto">
          <router-link to="/" class="logo">
            <img src="../assets/logo.png" alt="Logo" style="max-width: 55px;" />
          </router-link>
        </div>
        <div class="col-auto">
          <p class="copyright">
            &copy; <span id="copyYear">{{ new Date().getFullYear() }}</span>
            <router-link to="/"> EchoLink</router-link>. All Rights Reserved.
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>

export default {
  name: "FooterComponent",
  methods: {
   
    
  },
};
</script>


<style>
/*
.footer-two {
  background-image: url("~@/assets/images/footer-two-bg.png");
}

.home-two-light .footer-two {
  background-image: url("~@/assets/images/footer-two-bg.png");
}*/
</style>


