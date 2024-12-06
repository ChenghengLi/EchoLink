
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
    async get(id) {
        try {
            const response = await axios.get('/songs/' + id, UserService.getConfig());
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
    async update(id, data) {
        try {
            const response = await axios.put('/songs/' + id, data, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async delete(id) {
        try {
            const response = await axios.delete('/songs/' + id, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
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