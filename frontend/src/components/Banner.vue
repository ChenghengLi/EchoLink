<template>
    <div>
        <section class="section banner-one bg-img">
            <div class="container">
                <div class="row items-gap align-items-center">
                    <div class="col-12 col-md-10 col-lg-6">
                        <div class="banner-one__content">
                            <p class="h6">
                                <span>EchoLink</span>

                            </p>
                            <h2 class="h4">Connect with artists and other music fans worldwide. 
                                Join EchoLink now to share your music interests with the world</h2>
                            <div class="section__content-cta">
                                <a href="#learnMore" class="btn btn--primary">Learn More</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-lg-6">
                        <div class="banner-one__thumb text-start text-lg-end">
                            <img src="../images/img_dummy1.png" alt="Image" class="wow fadeInUp">
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>


export default {
    name: "Banner",
    methods: {

    }
};
</script>

<style scoped>
.home-light .banner-one {
    background-image: url('~@/assets/images/banner/banner-one-bg-light.png');
}

.home-dark .banner-one {
    background-image: url('~@/assets/images/banner/banner-one-bg.png');
}
</style>