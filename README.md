# Django JWT Authentication with Phone Number

This project implements a custom authentication system using Django and Django Rest Framework. It uses phone numbers for user identification and JWT (JSON Web Tokens) for session management.

## Features

- User registration with phone number
- OTP verification (currently using a hardcoded OTP for testing)
- JWT token generation and verification
- Protected routes using custom permission classes

## Prerequisites

- Python 3.12
- Django 5.0.1
- Django Rest Framework 3.14.0
- djangorestframework-simplejwt 5.3.1

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## requirements.txt

The project dependencies are listed in the `requirements.txt` file:
