import axios from './baseAxiosClient';

class ArtistService{
    async getArtists() {
        try {
            const response = await axios.get('/artists/');
            return response.data;
        } catch (error) {
            console.error('Error fetching artists:', error);
        }
    }
    
}

export default new ArtistService()