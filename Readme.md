
# EchoLink

EchoLink is a full-stack application featuring a FastAPI backend, a Vue.js frontend powered by Vite, and a PostgreSQL database managed with PgAgent. This README provides instructions on how to set up and run the project, as well as guidelines for contributing to the codebase.

## Table of Contents

- [Project Overview](#project-overview)
- [Clone the Repository](#clone-the-repository)
- [Running the Application with Docker Compose](#running-the-application-with-docker-compose)
- [Running Frontend and Backend Separately](#running-frontend-and-backend-separately)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Working Flow](#working-flow)
- [Contributors](#contributors)

## Project Overview

EchoLink is designed to provide a seamless user experience with a robust backend and a dynamic frontend. The project leverages FastAPI for its backend services, Vue.js with Vite for the frontend, and PostgreSQL for data storage.

## Clone the Repository

To get started with EchoLink, clone the repository from GitHub:

```bash
git clone https://github.com/UB-ES-2024-F3/EchoLink.git
cd EchoLink
```

## Running the Application with Docker Compose

To build and run the entire application using Docker Compose:

1. **Ensure Docker and Docker Compose are installed on your machine.**

2. **Navigate to the root directory of the project:**

   ```bash
   cd EchoLink
   ```

3. **Build and start the containers:**

   ```bash
   docker-compose up --build
   ```

4. **Access the application:**

   - The frontend will be available at `http://localhost:80`
   - The backend API will be available at `http://localhost:8000`
   - Access pgAdmin for database management at `http://localhost:5050`
     - **Login Credentials:**
       - Email: `admin@admin.com`
       - Password: `admin`



## Running Frontend and Backend Separately

### Backend Setup

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI server:**

   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install the dependencies:**

   ```bash
   npm install
   ```

3. **Run the development server:**

   ```bash
   npm run dev
   ```

## Working Flow

1. **Branching Strategy:**

   - For each issue, create a branch named as `assignee_issuenumber`. For example, if the assignee is John and the issue number is 42, the branch name should be `john_42`.
   - Assign the branch to the corresponding issue.

2. **Development Process:**

   - Work on the issue in the respective branch.
   - Once the task is completed, push the branch to the repository.

3. **Code Review and Merging:**

   - Open a pull request to merge the branch into the `master` branch.
   - The QA and Product Owner (PO) will review the code.
   - After approval, the code will be merged into the `master` branch.
   - Once merged, the issue will be closed, and the issue branch will be deleted.
     
## Contributors

- **Chengheng**: DevOps (Product Owner)
- **Pau**: QA
- **Gemma**: Frontend
- **Kamil**: Frontend
- **Diego**: Backend
- **Miquel**: Backend

