<template>
    <section class="section artists pb-0 pt-0">
        <div class="container">
            <div v-if="showHeader" class="row justify-content-center">
                <div class="col-12 col-xl-8">
                    <div data-wow-duration="600ms" data-wow-delay="300ms" class="section__header wow fadeInUp">
                        <h2 class="h2">Artists</h2>
                    </div>
                </div>
            </div>
            <div class="row justify-content-center">
                <div class="col-12 col-md-8">
                <input 
                    type="text" 
                    v-model="searchQuery" 
                    placeholder="Search for an artist..." 
                    class="form-control search-input"
                />
                </div>
            </div>

            <div class="row items-gap">
                <ArtistComponent
                v-for="artist in filteredArtists"
                :key="artist.id"
                :artist="artist"
                />
            </div>
        </div>
    </section>

  </template>
  
  <script>
  import ArtistComponent from './ArtistComponent.vue';
  import ArtistService from '../services/artist.js'

  export default {
    components: {
      ArtistComponent,
    },
    data() {
      return {
        // Lista de artistas, cada uno con propiedades "name", "genre" e "image"
        /*artists: [
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
        ],*/
        artists: [],
        searchQuery: '',
      };
    },
    computed: {
        filteredArtists() {
            const query = this.searchQuery.toLowerCase(); 
            if (!query) {
                return this.artists;
            }
            return this.artists.filter(
                artist =>
                artist.username.toLowerCase().includes(query) || // Filtrar por nombre
                artist.genre.toLowerCase().includes(query)  // Filtrar por género
            );
        },
    },
    methods: {
      async fetchArtists(){
        try {
          const data = await ArtistService.getArtists();
          const fixedImage = 'cara3.jpg';
          this.artists = data.map(artist => ({
            ...artist,
            image: fixedImage 
          }));
        } catch (error) {
          console.error('Error fetching artists:', error);
        }
      }
    },
    props: ['showHeader'],
    created(){
      this.fetchArtists();
    }
  };
  </script>

<style scoped>
.search-input {
  margin: 20px 0; 
  padding: 10px;
  font-size: 16px; 
  border: 1px solid #ddd; 
  border-radius: 5px; 
  outline: none;
  width: 100%; 
  box-shadow: none;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #4569e7; 
  box-shadow: 0 0 5px rgba(69, 105, 231, 0.5);
}
</style>
  
