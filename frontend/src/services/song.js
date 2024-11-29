
import axios from './baseAxiosClient';
import UserService from './user'

class SongService {
    async getAll() {
        try {
            const response = await axios.get('/songs/', UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
   async addSong(songInput) {
    axios.post('/songs', songInput)
    .then(response => {
        if (response && response.data) {
            console.log('Song created successfully:', response.data);
        } else {
            console.error('Unexpected response format:', response);
        }
    })
    .catch(error => {
        if (error.response) {
            console.error('Backend error:', error.response.data); // Error desde el servidor
        } else if (error.request) {
            console.error('No response received:', error.request); // El servidor no respondió
        } else {
            console.error('Error setting up the request:', error.message); // Error en el frontend
        }
    });
   }

    getConfig() {
        return {
            headers: {
                Authorization: `Bearer ${Cookies.get('auth_token')}`,
            }
        };
    }
}

export default new SongService()