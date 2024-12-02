
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
        try {
            const response = await axios.post('/songs', songInput, UserService.getConfig())
            return response.data
        } catch (err) {
            throw err;
        }
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