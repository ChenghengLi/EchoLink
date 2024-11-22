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
}

export default new PlaylistService()