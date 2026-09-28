# IT Career Backend API

A production-style backend API built with Python and FastAPI, featuring PostgreSQL database integration, JWT authentication, password hashing, validation, protected routes, CORS, and automated testing.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- bcrypt
- pytest
- Git & GitHub

## Features

- User registration
- User login with JWT authentication
- Secure password hashing
- Get all users
- Get a single user
- Update user
- Delete user
- Email validation
- Password validation
- Duplicate email handling
- Protected API endpoints
- API health check
- Database health check
- CORS configuration
- Automated tests

## Project Structure

```text
IT-Career/
├── python/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── auth.py
│   ├── dependencies.py
│   └── routers/
│       ├── auth.py
│       └── users.py
│
├── tests/
│   ├── test_health.py
│   ├── test_auth.py
│   └── test_users.py
│
├── .gitignore
└── README.md