<template>
    <section class="section artists pb-0">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-12 col-xl-8">
                    <div data-wow-duration="600ms" data-wow-delay="300ms" class="section__header wow fadeInUp">
                        <h2 class="h2">Artists</h2>
                    </div>
                </div>
            </div>
            <div class="row items-gap">
                <ArtistComponent
                    v-for="artist in artists"
                    :key="artist.id"
                    :artist="artist"
                />
            </div>
        </div>
    </section>

  </template>
  
  <script>
  import ArtistComponent from './ArtistComponent.vue';
  
  export default {
    components: {
      ArtistComponent,
    },
    data() {
      return {
        // Lista de artistas, cada uno con propiedades "name", "genre" e "image"
        artists: [
          {
            id: 1,
            name: 'Sam',
            genre: 'Rap',
            image: 'cara2.jpg',
          },
          {
            id: 2,
            name: 'John',
            genre: 'Pop',
            image: 'cara1.jpg',
          },
          {
            id: 3,
            name: 'Gracie',
            genre: 'Classic',
            image: 'cara3.jpg',
          },
          {
            id: 4,
            name: 'Shawn',
            genre: 'Pop',
            image: 'cara4.jpg',
          },
        ],
      };
    },
  };
  </script>
  
