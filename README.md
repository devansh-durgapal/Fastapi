# FastAPI User Authentication System

A secure user authentication and management API built with FastAPI, featuring JWT-based authentication, role-based access control, and password hashing with Argon2.

## Features

- ✅ User registration and authentication
- ✅ JWT token-based access control
- ✅ Secure password hashing with Argon2
- ✅ Role-based authorization
- ✅ Email validation
- ✅ SQLAlchemy ORM for database operations
- ✅ OAuth2 security implementation
- ✅ User profile management

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: SQLAlchemy ORM
- **Authentication**: JWT + OAuth2
- **Password Hashing**: Argon2 (via pwdlib)
- **Validation**: Pydantic
- **ASGI Server**: Uvicorn

## Project Structure

```
├── main.py           # FastAPI application entry point
├── user.py           # User routes and endpoints
├── auth.py           # Authentication logic (JWT, password hashing)
├── model.py          # SQLAlchemy database models
├── schema.py         # Pydantic schemas for request/response validation
├── database.py       # Database configuration and session management
├── config.py         # Application configuration settings
└── env/              # Python virtual environment
```

## Setup & Installation

### Prerequisites

- Python 3.13+
- pip

### Installation

1. **Activate the virtual environment**:
   ```bash
   source env/bin/activate
   ```

2. **Install dependencies** (if needed):
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings pwdlib pyjwt email-validator
   ```

3. **Configure environment variables** (create `.env` file):
   ```env
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   MAX_UPLOAD_SIZE=5242880
   ```

4. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /token` - Login with username and password
- `GET /me` - Get current user information (requires authentication)

### User Management

- `POST /create-user` - Create a new user
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user information
- `DELETE /users/{user_id}` - Delete a user

## Configuration

Settings are managed through environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | Required | Secret key for JWT token signing |
| `ALGORITHM` | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Token expiration time in minutes |
| `MAX_UPLOAD_SIZE` | 5MB | Maximum file upload size |

## Authentication Flow

1. User sends login credentials to `/token` endpoint
2. System verifies username and password
3. JWT token is generated and returned
4. Token is used in Authorization header for subsequent requests
5. Token is verified on protected endpoints

## Database Models

### UserData

```python
- id: Primary Key (Integer)
- username: Unique username (String, 50 chars max)
- name: Full name (String, 50 chars, optional)
- email: Unique email (String)
- password_hash: Hashed password (String, 255 chars)
- role: User role (String, 20 chars, default: "user")
```

## Security Features

- Passwords are hashed using Argon2
- JWT tokens for stateless authentication
- OAuth2 password bearer token security
- Email validation
- Role-based access control (RBAC)
- Secure token expiration

## Development

### Running Tests

```bash
# Tests can be added using pytest
pytest
```

### Code Style

Ensure code follows PEP 8 standards. Use:

```bash
pip install black flake8
black .
flake8 .
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please refer to the FastAPI documentation at https://fastapi.tiangolo.com/
