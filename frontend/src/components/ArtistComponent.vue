<template>
    <div class="col-12 col-md-6 col-xl-4">
      <div class="team-main-single wow fadeInUp" data-wow-duration="600ms" data-wow-delay="300ms">
        <div class="thumb">
            <img :src="`/images/${artist.image}`" :alt="artist.name" />
            <div class="content">
                <router-link :to="`/users/${artist.name}`" class="artist-link">
                    <h5 class="h5">{{ artist.name }}</h5>
                </router-link>
                <p>{{ artist.genre }}</p>
            </div>
        </div>
      </div>
    </div>
  </template>

<script>
export default {
  name: 'ArtistComponent',
  props: {
    artist: {
      type: Object,
      required: true,
    },
  },
};
</script>


<style scoped>
.team-main-single {
    width: 100%;
    max-width: 300px; 
    height: 400px;
    position: relative;
    overflow: hidden;
    margin: auto;
}

.thumb {
    position: relative;
    overflow: hidden;
}

.thumb img {
   width: 100%;
   min-height: 300px;
   object-fit: cover;
}

img {
    max-width: 100%;
    height: auto;
    object-fit: cover;
    border: 0;
    outline: 0;
    vertical-align: middle;
}

.content {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 30px;
    min-width: 100%;
    background: linear-gradient(
        to top,
        rgba(69, 105, 231, 1), 
        rgba(69, 105, 231, 0.9), 
        rgba(69, 105, 231, 0.8),
        rgba(255, 255, 255, 0)   
    );
    color: white;
    box-sizing: border-box;
    opacity: 0;
    transition: opacity 0.4s ease-in-out;
}

.content p,
.content h5{
    color: white;
}

.thumb:hover .content {
    opacity: 1;
}

</style>