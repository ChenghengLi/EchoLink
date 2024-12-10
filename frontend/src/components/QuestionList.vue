<template>
    <section class="section questions pb-0 pt-3">
      <div class="container">
        <!-- Header -->
        <div v-if="showHeader" class="row justify-content-center">
          <div class="col-12 col-xl-8">
            <div data-wow-duration="600ms" data-wow-delay="300ms" class="section__header wow fadeInUp">
              <h2 ref="questionsHeader" class="h2">Questions</h2>
            </div>
          </div>
        </div>
  
        <!-- Search -->
        <div class="row justify-content-center align-items-center mb-4">
          <div class="col-12 col-md-6 d-flex justify-content-center align-items-center search-container">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search for a question..."
              class="form-control search-input"
            />
          </div>
        </div>
  
        <!-- Questions List -->
        <div class="row items-gap">
          <QuestionCard
            v-for="question in filteredQuestions"
            :key="question.id"
            :question="question"
            @archived="archiveQuestion(question.id)"
          />
        </div>
      </div>
    </section>
  </template>
  
  <script>
  import QuestionCard from './QuestionCard.vue'; 
  import QuestionService from '../services/questions.js'; 


  export default {
    components: {
      QuestionCard,
    },
    data() {
      return {
        questions: [], // Array of questions
        searchQuery: '',
      };
    },
    computed: {
      filteredQuestions() {
        const query = this.searchQuery.toLowerCase();
        return this.questions.filter((question) =>
          question.question_text.toLowerCase().includes(query)
        );
      },
    },
    methods: {
      archiveQuestion(id) {
        const questionIndex = this.questions.findIndex((q) => q.id === id);
        if (questionIndex !== -1) {
          this.questions[questionIndex].archived = true;
        }
      },
      async fetchQuestions() {
        // Fetch questions from an API or service
        try {
            console.log("Fetching questions...");
          const data = await QuestionService.getUserQuestions();
          console.log('Questions:', data);

          this.questions = data.questions;
        } catch (error) {
          console.error('Error fetching questions:', error);
        }
      },
    },
    props: {
      showHeader: Boolean,
    },
    created() {
      this.fetchQuestions();
    },
  };
  </script>
  
  <style scoped>
  .search-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
  }
  
  .search-input {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-radius: 5px;
    outline: none;
    width: 100%;
    max-width: 400px;
    transition: all 0.3s ease;
  }
  
  .search-input:focus {
    border-color: #4569e7;
    box-shadow: 0 0 5px rgba(69, 105, 231, 0.5);
  }
  
  .items-gap {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  </style>