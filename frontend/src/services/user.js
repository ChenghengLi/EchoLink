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
    async get(username) {
        try {
            // TODO replace this once user endpoint is ready
            // const response = await axios.get('/users/' + username);
            // return response.data;
            return {description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum", genre: 'some genre', visibility: true}
        } catch (error) {
            throw error;
        }
    }
    isLoggedIn() {
        return Cookies.get('logged_in') || true // TODO replace once sessions are implemented
    }
}

export default new UserService()