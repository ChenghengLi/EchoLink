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
                            <h1 class="h1">Music For Everyone</h1>
                            <div class="section__content-cta">
                                <a href="#learnMore" class="btn btn--primary">Learn More</a>
                                <!--<button class="btn btn--primary">
                                    Learn More
                                </button>-->
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
    <section class="section broadcast pb-0">
        <div class="container">
            <div class="row">
                <div class="col-12 fix-scroll">
                    <div data-wow-duration="600ms" class="broadcast__inner wow fadeInUp" style="visibility: visible; animation-duration: 600ms;">
                        <div class="row align-items-center itemps-gap-two">
                            <div class="col-12 col-xl-8 col-xxl-7">
                                <div class="section__content broadcast__inner-content" id="learnMore">
                                    <h2 class="h2">What is EchoLink</h2>
                                    <div class="paragraph">
                                        <p>
                                            PROVA PROVA PROVA PROVA
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-xl-4 col-xxl-5">
                                <div class="broadcast__thumb text-xl-center">
                                    <img src="../images/img_dummy1.png" alt="Image">
                                </div>
                            </div>
                        </div>
                    </div> 
                    <div data-wow-duration="600ms" class="broadcast__inner wow fadeInUp" style="visibility: visible; animation-duration: 600ms;">
                        <div class="row align-items-center itemps-gap-two">
                            <div class="col-12 col-xl-4 col-xxl-5">
                                <div class="broadcast__thumb text-xl-center">
                                    <img src="../images/img_dummy1.png" alt="Image">
                                </div>
                            </div>
                            <div class="col-12 col-xl-8 col-xxl-7">
                                <div class="section__content broadcast__inner-content">
                                    <h2 class="h2">What is EchoLink</h2>
                                    <div class="paragraph">
                                        <p>
                                            PROVA PROVA PROVA PROVA
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div data-wow-duration="600ms" class="broadcast__inner wow fadeInUp" style="visibility: visible; animation-duration: 600ms;">
                        <div class="row align-items-center itemps-gap-two">
                            <div class="col-12 col-xl-8 col-xxl-7">
                                <div class="section__content broadcast__inner-content">
                                    <h2 class="h2">What is EchoLink</h2>
                                    <div class="paragraph">
                                        <p>
                                            PROVA PROVA PROVA PROVA
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-xl-4 col-xxl-5">
                                <div class="broadcast__thumb text-xl-center">
                                    <img src="../images/img_dummy1.png" alt="Image">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
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