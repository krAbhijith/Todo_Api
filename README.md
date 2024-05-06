# Todo API Project

Welcome to the Todo API project! This API is built using Django REST Framework with JWT authentication. It allows users to manage their todo tasks through a RESTful API.

## Installation

To get started with the Todo API project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/todo-api.git
   cd todo-api

# Usage

## Authentication

- **Register a new user**:
  - **POST** request to `http://localhost:8000/api/auth/register/` with `username`, `email`, and `password` in the request body.
- **Obtain a JWT token**:
  - **POST** request to `http://localhost:8000/api/auth/login/` with `username` and `password` in the request body. Copy the token from the response.
- **Use the token for authenticated requests**:
  - Include the token in the Authorization header as `Bearer YOUR_TOKEN` for all authenticated endpoints.

## API Endpoints

- **GET** `/api/todos/`: List all todos (requires authentication).
- **POST** `/api/todos/`: Create a new todo (requires authentication).
- **GET** `/api/todos/<id>/`: Retrieve a specific todo (requires authentication).
- **PUT** `/api/todos/<id>/`: Update a specific todo (requires authentication).
- **DELETE** `/api/todos/<id>/`: Delete a specific todo (requires authentication).

## Testing

Run the automated tests to ensure everything is working correctly:

```bash
python manage.py test

