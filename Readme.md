# EchoLink

EchoLink is a full-stack application featuring a FastAPI backend, a Vue.js frontend powered by Vite, and a PostgreSQL database managed with PgAgent. This README provides instructions on how to set up and run the project, as well as guidelines for contributing to the codebase.

## Table of Contents

- [Project Overview](#project-overview)
- [Clone the Repository](#clone-the-repository)
- [Running the Application with Docker Compose](#running-the-application-with-docker-compose)
- [Accessing PgAgent](#accessing-pgagent)
- [Running Frontend and Backend Separately](#running-frontend-and-backend-separately)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running Tests](#running-tests)
  - [Backend Tests](#backend-tests)
  - [Frontend Tests](#frontend-tests)
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
   - Access pgAdmin for database management at `http://localhost:8001`
     - **Login Credentials:**
       - Email: `admin@admin.com`
       - Password: `admin`

## Accessing PgAgent

If the server does not appear in pgAdmin, you can manually add it by following these steps:

1. **Click on "Add Server":**

2. **In the "General" tab:**
   - Set the **Name** field to `EchoLink`.

3. **In the "Connection" tab:**
   - **Host name/address**: `postgres`
   - **Username**: `user`
   - **Password**: `password`
   - Activate the **Save password** option.

4. **Click "Save"** to add the server.

## Running Frontend and Backend Separately

> [!WARNING]
> When running the frontend and backend separately, you are running them locally and not within Docker containers. 
> This approach is **not recommended** due to potential configuration issues and discrepancies between development and production environments. 
> It is preferable to use Docker Compose to ensure consistency and proper environment setup.

### Backend Setup

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Navigate to the app folder:**

   ```bash
   cd app
   ```

4. **Change to the local path for the database at database/config.py:**

   ```bash
   URL_DATABASE_LOCAL = "postgresql://user:password@localhost:5432/Echolink"
   ```

   Reminder changing it back when running in docker, the database should be running in docker.

5. **Run the FastAPI server:**

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

## Running Tests

### Backend Tests

**Introduction:**  
All tests are automatically executed within the Dockerfiles when building the application. However, if you would like to run the tests during development, particularly for the backend, you have two options.

#### Option 1: Running Tests Using Docker UI

1. **Access the Docker Dashboard:**

   Open the Docker Desktop application on your machine. This provides a graphical user interface to manage your Docker containers.

2. **Locate the Backend Container:**

   In the Docker Dashboard, find the container running the backend service. It should be listed among the active containers.

3. **Open a Terminal Session:**

   Use the Docker UI to open a terminal session within the backend container. This option is usually available as a "CLI" or "Terminal" button in the container's details view.

4. **Run Pytest:**

   Once inside the container's terminal, navigate to the directory containing the tests, if needed, and execute Pytest:

   ```bash
   pytest ./tests
   ```

#### Option 2: Running Tests Using Docker Exec

1. **Identify the Backend Container:**

   Start by listing the running containers to find the backend container's ID or name:

   ```bash
   docker ps
   ```

2. **Execute Pytest from Your Host Machine:**

   Use `docker exec` to run Pytest directly from your host machine without entering the container:

   ```bash
   docker exec -it <container_id_or_name> pytest ./tests
   ```

### Frontend Tests

**Note:** Frontend tests are not yet implemented. Once implemented, instructions for running frontend tests will be provided here.

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
```