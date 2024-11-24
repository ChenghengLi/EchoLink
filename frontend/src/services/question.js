import axios from './baseAxiosClient';

class QuestionService{
    async newQuestion(artistUsername, questionText){
        try {
            const response = await axios.post('/questions', {
                'artist_username': artistUsername,
                'question_text': questionText,
            }, this.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    getConfig() {
        return {
            headers: {
                Authorization: `Bearer ${Cookies.get('auth_token')}`,
            }
        };
    }
}

export default new QuestionService()