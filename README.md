# Django JWT Authentication with Phone Number

This project implements a custom authentication system using Django and Django Rest Framework. It uses phone numbers for user identification and JWT (JSON Web Tokens) for session management.

## Features

- User registration with phone number
- OTP verification (currently using a hardcoded OTP for testing)
- JWT token generation and verification
- Protected routes using custom permission classes

## Prerequisites

- Python 3.12
- Poetry (for dependency management)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/djang-auth-service.git
   cd djang-auth-service
   ```

2. Set up the project using Make:
   ```
   make init
   ```
   This command will set up pyenv, create a virtual environment, and install all necessary dependencies using Poetry.

3. Activate the virtual environment:
   ```
   pyenv activate djang-auth-service
   ```

4. Apply migrations:
   ```
   make migrate
   ```

5. Create a superuser (optional):
   ```
   make superuser
   ```

6. Run the development server:
   ```
   make run
   ```

## Available Make Commands

- `make help`: Display all available make commands
- `make install`: Install dependencies using Poetry
- `make update`: Update dependencies
- `make run`: Run the development server
- `make test`: Run tests
- `make lint`: Check code with linters (flake8 and mypy)
- `make clean`: Clean cache and temporary files
- `make commit`: Create a commit using Commitizen
- `make bump`: Bump the project version
- `make release`: Create a new release

## Project Structure

The main components of the project are:

- `auth_project/`: The main Django project directory
- `users/`: The Django app handling user authentication
- `users/models.py`: Contains the custom user model
- `users/views.py`: Implements the authentication views
- `users/serializers.py`: Defines serializers for user data
- `users/permissions.py`: Custom permission classes

## API Endpoints

- `/api/register/`: User registration
- `/api/verify-otp/`: OTP verification
- `/api/token/`: Obtain JWT tokens
- `/api/token/verify/`: Verify JWT tokens
- `/api/protected/`: A protected view (requires authentication)

## Development

This project uses Poetry for dependency management and Commitizen for standardized commit messages. To contribute:

1. Make your changes
2. Run tests: `make test`
3. Check linting: `make lint`
4. Commit changes: `make commit`
5. Create a pull request

## License

[Specify your license here]
