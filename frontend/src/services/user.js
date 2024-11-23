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
            const data = response.data;
            const token = data.access_token;
            const username = data.username;

            if (!token) {
                throw new Error('Token not found in the response.');
            }

            Cookies.set('auth_token', token, {expires: 7});
            Cookies.set('username', username, {expires: 7});
            Cookies.set('logged_in', 'true', {expires: 7}) // Expire login flag after 7 days

            return response;
        } catch (error) {
            throw error;
        }
    }
    async logout() {
        try {
            const response = await axios.post('/login/logout', {}, this.getConfig());
            return response.data; 
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
    deleteAccount(){
        return axios.delete('/users/user', this.getConfig())
        .then(response => {
            return response.data;
        })
        .catch(error => {
            throw error.response ? error.response.data : new Error('Error deleting account');
        });
    }
    getUserRole(){
        /*return axios.get('/users/role')
        .then(response => {
            return response.data;
        })
        .catch(error => {
            throw error.response ? error.response.data : new Error('Error getting role');
        });*/
        const config = this.getConfig(); // Obtiene la configuración del token
        console.log("Config enviada al backend:", config); // Verifica el encabezado

        return axios.get('/users/role', config)
            .then(response => {
                console.log("Respuesta del backend:", response.data); // Depura la respuesta
                return response.data;
            })
            .catch(error => {
                console.error("Error al obtener el rol:", error.response ? error.response.data : error);
                throw error.response ? error.response.data : new Error('Error getting role');
            });
    }
}

export default new UserService()