<template>
  <footer class="footer-two section bg-img">
    <div class="container">
      <div class="row items-gap-two">
        <!--<div class="col-12 col-sm-6 col-xl-6 col-xxl-5">-->
        <div class="col-10 col-sm-10 col-xl-10 col-xxl-10">
          <!--<div class="footer-two__single bt wow fadeInUp" data-wow-duration="600ms">-->
          <div class="footer-two__single wow fadeInUp" data-wow-duration="600ms">
            <router-link to="/" class="logo">
              <img src="../assets/logo.png" alt="Image" />
            </router-link>
            <p>
              Copyright &copy;
              <span id="copyYear">{{ new Date().getFullYear() }}</span>
              <a href="/" aria-current="page" class="router-link-exact-active router-link-active">EchoLink</a>
              <router-link to="/">  EchoLink</router-link>
              . All Rights Reserved.
            </p>
          </div>
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


