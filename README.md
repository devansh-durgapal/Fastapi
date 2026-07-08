# FastAPI User Authentication System
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

## API Endpoints

### Authentication

- `POST /token` - Login with username and password
- `GET /me` - Get current user information (requires authentication)


## Configuration

Settings are managed through environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | Required | Secret key for JWT token signing |
| `ALGORITHM` | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Token expiration time in minutes |
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
- Role-based access control (RBAC)
- Secure token expiration
