# FastAPI Authentication Service

A FastAPI-based authentication service with OAuth2/JWT token-based authentication, SQLAlchemy ORM, and PostgreSQL database integration.

## Features

- User registration and authentication
- JWT token-based authentication
- Password hashing with bcrypt
- PostgreSQL database integration
- SQLAlchemy ORM with Alembic migrations

## API Endpoints

- `POST /register` - Register a new user
- `POST /token` - Login and get access token
- `GET /me` - Get current user information (protected)

## Requirements

- Python 3.13+
- PostgreSQL
- Environment variables:
  - `DATABASE_URL`: PostgreSQL connection string
  - `SECRET_KEY`: JWT signing key
  - `ALGORITHM`: JWT algorithm (typically HS256)
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Installation and Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env` file or export them:
```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
export SECRET_KEY="your-secret-key"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

### Development Server
```bash
# Option 1: Using uvicorn directly
python -m uvicorn app.main:app --reload

# Option 2: Using the main script
python app/main.py
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

## Running Tests

### Install Development Dependencies
```bash
pip install -e ".[dev]"
```

### Run Tests
```bash
# Using pytest directly
pytest tests/ -v

# Using nox (recommended)
nox -s tests

# Run linting
nox -s lint

# Format code
nox -s format_code
```

## API Usage Examples

### 1. Register a New User
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Login (Get Access Token)
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get Current User Information (Protected)
```bash
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com"
}
```

### Error Responses

**401 Unauthorized (Invalid credentials):**
```json
{
  "detail": "Incorrect email or password"
}
```

**400 Bad Request (Email already registered):**
```json
{
  "detail": "Email already registered"
}
```

**401 Unauthorized (Invalid token):**
```json
{
  "detail": "Could not validate credentials"
}
```

## Database Operations

### Create New Migration
```bash
alembic revision --autogenerate -m "migration_name"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```