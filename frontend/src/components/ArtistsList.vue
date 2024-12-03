<template>
  <section class="section artists pb-0 pt-3">
    <div class="container">
      <!-- Header -->
      <div v-if="showHeader" class="row justify-content-center">
        <div class="col-12 col-xl-8">
          <div data-wow-duration="600ms" data-wow-delay="300ms" class="section__header wow fadeInUp">
            <h2 class="h2">Artists</h2>
          </div>
        </div>
      </div>

      <!-- Search and Order By -->
      <div class="row justify-content-center align-items-center mb-4">
        <div class="col-12 col-md-6 d-flex justify-content-center align-items-center search-container">
          <input type="text" v-model="searchQuery" placeholder="Search for an artist..."
            class="form-control search-input" />
          <div class="dropdown ms-3">
            <button class="btn btn-primary dropdown-toggle selector-btn" type="button" id="orderByDropdown"
              data-bs-toggle="dropdown" aria-expanded="false">
              Sort By: {{ sortOrder }}
            </button>
            <ul class="dropdown-menu" aria-labelledby="orderByDropdown">
              <li><a class="dropdown-item" @click="setSortOrder('Alphabet')">By Alphabet</a></li>
              <li><a class="dropdown-item" @click="setSortOrder('Engagement')">By Engagement</a></li>
              <li><a class="dropdown-item" @click="setSortOrder('Followers')">By Followers</a></li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Artists List -->
      <div class="row items-gap">
        <ArtistComponent v-for="artist in paginatedArtists" :key="artist.id" :artist="artist" />
      </div>

      <!-- Pagination -->
      <div class="row justify-content-center mt-4">
        <div class="col-auto">
          <nav>
            <ul class="pagination">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="changePage(currentPage - 1)">Previous</button>
              </li>
              <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
                <button class="page-link" @click="changePage(page)">{{ page }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="changePage(currentPage + 1)">Next</button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import ArtistComponent from './ArtistComponent.vue';
import ArtistService from '../services/artist.js'; // Assume this service handles API calls

import fixedImage from '../assets/images/cara1.jpg'; // Default image for artists without an image

export default {
  components: {
    ArtistComponent,
  },
  data() {
    return {
      artists: [],
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 9,
      sortOrder: 'Alphabet', // Default sort order
    };
  },
  computed: {
    filteredArtists() {
      const query = this.searchQuery.toLowerCase();
      let filtered = this.artists;
      console.log(this.artists)

      if (query) {
        filtered = filtered.filter(
          artist =>
            artist.username.toLowerCase().includes(query)
        );
      }

      return filtered;
    },
    totalPages() {
      return Math.ceil(this.filteredArtists.length / this.itemsPerPage);
    },
    paginatedArtists() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredArtists.slice(start, end);
    },
  },
  methods: {
    async fetchArtists() {
      try {
        // Fetch artists from the backend based on the selected sort order
        const data = await ArtistService.getArtistsByAlphabet();
        this.artists = data.map(artist => ({
          ...artist,
          image: artist.image_url || fixedImage,
        }));
      } catch (error) {
        console.error('Error fetching artists:', error);
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.scrollToTop(); // Scroll to top when page changes
      }
    },
    async setSortOrder(order) {
      this.sortOrder = order;
      this.currentPage = 1; // Reset to the first page after sorting
      let data = null;
      try {
        switch (order) {
          case 'Engagement':
            data = await ArtistService.getArtistByEngagement();
            break;
          case 'Followers':
            data = await ArtistService.getArtistByFollowers();
            break;
          default:
            data = await ArtistService.getArtistsByAlphabet();
            break;
        }
        console.log(data)
        this.artists = data.map(artist => ({
          ...artist,
          image: artist.image_url || fixedImage,
        }));
      } catch (error) {
        console.error('Error fetching artists:', error);
      }
      this.scrollToTop(); // Scroll to top after sorting
    },
    scrollToTop() {
      const section = this.$el; // Get the root element of the component
      section.scrollIntoView({ behavior: 'smooth', block: 'start' }); // Smooth scroll to the top
    },
  },
  props: {
    showHeader: Boolean,
  },
  created() {
    this.setSortOrder("Alphabet");
  },
};
</script>

<style scoped>
.search-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  /* Space between search bar and dropdown */
}

.search-input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
  width: 100%;
  max-width: 400px;
  /* Centered and responsive */
  box-shadow: none;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #4569e7;
  box-shadow: 0 0 5px rgba(69, 105, 231, 0.5);
}

.selector-btn {
  padding: 10px 15px;
  font-size: 16px;
  border-radius: 5px;
  background-color: #4569e7;
  border: none;
  color: white;
  transition: background-color 0.3s ease;
}

.selector-btn:hover {
  background-color: #3457c5;
}

.dropdown-menu {
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.pagination {
  display: flex;
  list-style: none;
  padding: 0;
}

.page-item {
  margin: 0 5px;
}

.page-item .page-link {
  border: 1px solid #ddd;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.page-item.active .page-link {
  background-color: #4569e7;
  color: white;
  border-color: #4569e7;
}

.page-item.disabled .page-link {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>