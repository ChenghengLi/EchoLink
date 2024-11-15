import axios from './baseAxiosClient';
import Cookies from 'js-cookie'

class UserService {
    async registerAccount(username, email, password) {
        try {
            const response = await axios.post('/users/user', {
                'username': username,
                'email': email,
                'password': password,
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async loginAccount(email, password) {
        try{
            const response = await axios.post('/login', {
                'email': email,
                'password': password,
            });
            return response;
        } catch (error) {
            throw error;
        }
    }
    async updateProfile(data) {
        try {
            const response = await axios.put('/users/user', data, this.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async get(username) {
        try {
            const response = await axios.get('/users/' + username);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    isLoggedIn() {
        return (Cookies.get('auth_token') !== undefined) && (Cookies.get('username') !== undefined) // Checks both cookies for coherency.
    }
    // Returns the username of the current session,
    // or null if the client is not logged in.
    getCurrentUsername() {
        return this.isLoggedIn() ? Cookies.get('username') : null // Tests for both cookies as sanity check.
    }
    getConfig() {
        return {
            headers: {
                Authorization: `Bearer ${Cookies.get('auth_token')}`,
            }
        };
    }
}

export default new UserService()