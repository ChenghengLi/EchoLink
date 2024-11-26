<template>
    <div class="col-12 col-md-6 col-xl-4">
      <div class="team-main-single wow fadeInUp" data-wow-duration="600ms" data-wow-delay="300ms">
        <div class="thumb">
            <router-link :to="`/users/${artist.username}`">
                <img :src="`frontend/src/assets/images/${artist.image}`" :alt="artist.name" class="clickable-image" />
            </router-link>
            <div class="content">
                <h5 class="h5">{{ artist.username }}</h5>
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
.col-12.col-md-6.col-xl-4 {
  display: flex; 
  justify-content: center; 
  align-items: center; 
}

.team-main-single {
    width: 100%;
    max-width: 100%; 
    height: auto; 
    margin-bottom: 20px; 
}

.thumb {
    position: relative;
    overflow: hidden;
}

.thumb img {
    width: 100%;
    height: auto; 
    min-height: 300px; 
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

.clickable-image {
  transition: transform 0.3s ease, opacity 0.3s ease; 
}

.clickable-image:hover {
  transform: scale(1.05); 
  opacity: 0.9; 
}

</style>