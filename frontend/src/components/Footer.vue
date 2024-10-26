<template>
  <footer class="footer-two section bg-img">
    <div class="container">
      <div class="row items-gap-two">
        <div class="col-12 col-sm-6 col-xl-4 col-xxl-5">
          <div class="footer-two__single bt wow fadeInUp" data-wow-duration="600ms">
            <router-link to="/" class="logo">
              <img src="" alt="Image" />
            </router-link>
            <p>
              Copyright &copy;
              <span id="copyYear">{{ new Date().getFullYear() }}</span>
              <router-link to="/">  EchoLink</router-link>
              . All Rights Reserved.
            </p>
            <!--<div class="social">
              <a href="https://www.facebook.com" aria-label="social media">
                <i class="fa-brands fa-facebook-f"></i>
              </a>
              <a href="https://www.linkedin.com" aria-label="social media">
                <i class="fa-brands fa-linkedin-in"></i>
              </a>
              <a href="https://www.instagram.com" aria-label="social media">
                <i class="fa-brands fa-instagram"></i>
              </a>
            </div>--->
          </div>
        </div>
        <div class="col-12 col-sm-6 col-xl-2 col-xxl-2">
          <div class="footer-two__single wow fadeInUp" data-wow-duration="600ms" data-wow-delay="200ms">
            <h5 class="h5">Resources</h5>
            <ul>
              <li>
                <a href="/">Link</a>
              </li>
           
            </ul>
          </div>
        </div>
        <div class="col-12 col-sm-6 col-xl-2 col-xxl-2">
          <div class="footer-two__single wow fadeInUp" data-wow-duration="600ms" data-wow-delay="400ms">
            <h5 class="h5">Activities</h5>
            <ul>
              <li>
                <a href="javascript:void(0)">Upcoming</a>
              </li>
            </ul>
          </div>
        </div>
        <div class="col-12 col-sm-6 col-xl-4 col-xxl-3">
          <div class="footer-two__single wow fadeInUp" data-wow-duration="600ms" data-wow-delay="600ms">
            <div class="footer-two__form">
              <h6 class="h6">Subscribe to Our Newsletter for Events & Activities!</h6>
              <form @submit="subscribeToNewsletter" method="post">
                <div class="mail-group">
                  <input type="email" name="subscribe-news" id="subscribeNews" placeholder="Enter your email"
                    required />
                  <button type="submit" aria-label="subscribe to our newsletter">
                    <i class="fa-regular fa-paper-plane"></i>
                  </button>
                </div>
              </form>

            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>


export default {
  name: "Footer2",
  methods: {
   
    
  }
};
</script>


<style>
.footer-two {
  background-image: url("~@/assets/images/footer-two-bg.png");
}

.home-two-light .footer-two {
  background-image: url("~@/assets/images/footer-two-bg-light.png");
}
</style>
