import axios from './baseAxiosClient';

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
}

export default new UserService()