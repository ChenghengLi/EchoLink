// TODO readd when integrating API
import axios from './baseAxiosClient';
import UserService from './user'

class SongService {
    async getAll() {
        try {
            // const response = await axios.get('/songs/' + id, UserService.getConfig());
            // return response.data;
            // TODO remove once API is done
            const response = {
                songs: [
                    {id: 1, artist: 'some artist', title: 'some song', duration: 124, genre: 'test'},
                    {id: 2, artist: 'some artist 2', title: 'some title 2', duration: 144, genre: 'test'},
                    {id: 3, artist: 'some artist 3', title: 'some title 3', duration: 114, genre: 'test2'},
                    {id: 4, artist: 'some artist 4', title: 'some title 4', duration: 84, genre: 'test'},
                    {id: 5, artist: 'a song you can add 2', title: 'some title asdasd', duration: 84, genre: 'test2'},
                    {id: 6, artist: 'a song you can add', title: 'some title 5', duration: 84, genre: 'test3'},
                ]
            }
            return response
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