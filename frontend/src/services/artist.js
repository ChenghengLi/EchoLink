import axios from './baseAxiosClient';
import Cookies from 'js-cookie'

class ArtistService{
    async getArtistsByAlphabet() {
        try {
            const response = await axios.get('/artists/');
            return response.data;
        } catch (error) {
            console.error('Error fetching artists:', error);
        }
    }

    async getArtistByEngagement() {
        try {
            const response = await axios.get('/artists/engagement');
            return response.data;
        } catch (error) {
            console.error('Error fetching artists:', error);
        }
    }

    async getArtistByFollowers() {
        try {
            const response = await axios.get('/artists/followers');
            return response.data;
        } catch (error) {
            console.error('Error fetching artists:', error);
        }
    }


    async getFollowers() {
        try {
            const response = await axios.get('/metrics/followers',  {
                params: {
                    'artist_name': Cookies.get('username') 
                }
            }
            );
            return response.data;
        } catch (error) {
            console.error('Error fetching followers:', error);
        }
    }

    async getEngagementRate() {
        try {
            const response = await axios.get('/metrics/engagement_rate', {
                params: {
                    'artist_name': Cookies.get('username') 
                }
            }
            );
            return response.data;
        } catch (error) {
            console.error('Error fetching engagemen rate:', error);
        }
    }

    async getResponseRate() {
        try {
            const response = await axios.get('/metrics/response_rate', {
                params: {
                    'artist_name': Cookies.get('username') 
                }
            }
        );
            return response.data;
        } catch (error) {
            console.error('Error fetching response rate:', error);
        }
    }

    async getRanking() {
        try {
            const response = await axios.get('/metrics/ranking', {
                params: {
                    'artist_name': Cookies.get('username') 
                }
            }
        );
            return response.data;
        } catch (error) {
            console.error('Error fetching response rate:', error);
        }
    }
    
}

export default new ArtistService()