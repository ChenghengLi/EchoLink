import axios from './baseAxiosClient';
import UserService from './user'

class ListenerService {
    async checkFollow(artistName) {
        try {
            const response = await axios.get(`/listeners/follows/${artistName}`, UserService.getConfig());
            return response.data.follows;
        } catch (error) {
            throw error.response ? error.response.data : new Error('Error checking follow status');
        }
    }
    async follow(artistName){
        try {
            const response = await axios.post(`/listeners/follow/${artistName}`, {}, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : new Error('Error following artist');
        }
    }
    async unfollow(artistName){
        try {
            const response = await axios.post(`/listeners/unfollow/${artistName}`, {}, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : new Error('Error unfollowing artist');
        }
    }
    
}

export default new ListenerService()