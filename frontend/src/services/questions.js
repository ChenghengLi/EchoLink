import axios from './baseAxiosClient';
import UserService from './user'

class QuestionService {
    // Retrieves the questions asked to the logged-in user (if they are an artist)
    // or asked by the user (if they are a listener)
    async getUserQuestions() {
        try {
            const response = await axios.get('/questions/questions', UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default new QuestionService()