// TODO readd when integrating API
// import axios from './baseAxiosClient';
// import UserService from './user'

class SongService {
    async getAll() {
        try {
            // const response = await axios.get('/songs/' + id, UserService.getConfig());
            // return response.data;
            // TODO remove once API is done
            const response = {
                songs: [
                    {id: 1, artist: 'some artist', title: 'some song', duration: 124},
                    {id: 2, artist: 'some artist 2', title: 'some title 2', duration: 144},
                    {id: 3, artist: 'some artist 3', title: 'some title 3', duration: 114},
                    {id: 4, artist: 'some artist 4', title: 'some title 4', duration: 84},
                    {id: 5, artist: 'a song you can add 2', title: 'some title asdasd', duration: 84},
                    {id: 6, artist: 'a song you can add', title: 'some title 5', duration: 84},
                ]
            }
            return response
        } catch (error) {
            throw error;
        }
    }
}

export default new SongService()