import axios from './baseAxiosClient';
import UserService from './user'

class PlaylistService {
    async createPlaylist(data) {
        try {
            // TODO adjust once specifications are final
            const response = await axios.post('/users/playlists/', data, UserService.getConfig());
            return response.data;
        } catch (err) {
            throw new Error(err.response ? err.response.data.detail : err.message); // Fallback to HTTP error message if no detail is provided.
        }
    }
    async update(data) {
        try {
            const response = await axios.put('/users/playlists', data, UserService.getConfig());
    async delete(id) {
        try {
            const response = await axios.delete('/playlist/' + id, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async get(id) {
        try {
            const response = await axios.get('/playlist/' + id, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async getUserPlaylists(username) {
        try {
            const response = await axios.get('/playlist/user/' + username, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default new PlaylistService()