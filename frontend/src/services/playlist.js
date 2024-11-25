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
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async get(id) {
        try {
            // const response = await axios.get('/users/playlists/' + id, UserService.getConfig());
            // return response.data;
            // TODO remove once API is done
            const response = {
                id: id,
                name: 'test playlist',
                description: 'dummy descp',
                visibility: 'public',
                owner: 'pip',
                songs: [
                    {id: 1, artist: 'some artist', title: 'some title', duration: 124},
                    {id: 2, artist: 'some artist 2', title: 'some title 2', duration: 144},
                    {id: 3, artist: 'some artist 3', title: 'some title 3', duration: 114},
                    {id: 4, artist: 'some artist 4', title: 'some title 4', duration: 84},
                ]
            }
            return response
        } catch (error) {
            throw error;
        }
    }
}

export default new PlaylistService()