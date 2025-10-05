# Books & Articles API

A FastAPI application for managing books and articles with SQLite database using SQLAlchemy, featuring JWT authentication and authorization.

## Features

- **CRUD Operations**: Create, Read, Update, Delete books and articles
- **JWT Authentication**: Secure user authentication with JWT tokens
- **Authorization**: Role-based access control (regular users vs superusers)
- **User Management**: User registration, login, and profile management
- **Search**: Search books by title/author, articles by title/author/content
- **Pagination**: Get books and articles with pagination support
- **Advanced Filtering**: Filter articles by category and publication status
- **ISBN Support**: Unique ISBN validation for books
- **Data Validation**: Pydantic models for request/response validation
- **Auto Documentation**: Interactive API docs with Swagger UI
- **SQLite Database**: Lightweight database with SQLAlchemy ORM
- **Modular Architecture**: Organized route, model, and schema structure for scalability

## Project Structure

```
books-api/
├── main.py              # FastAPI application entry point
├── auth.py              # JWT authentication utilities
├── models/              # Modular model structure
│   ├── __init__.py      # Model package initialization
│   ├── base.py          # SQLAlchemy Base class
│   ├── book.py          # Book model
│   ├── article.py       # Article model
│   └── user.py          # User model
├── schemas/             # Modular schema structure
│   ├── __init__.py      # Schema package initialization
│   ├── book.py          # Book-related Pydantic schemas
│   ├── article.py       # Article-related Pydantic schemas
│   └── user.py          # User-related Pydantic schemas
├── database.py          # Database configuration and connection
├── routes/              # Modular route structure
│   ├── __init__.py      # Route package initialization
│   ├── books.py         # Book-related API endpoints
│   ├── articles.py      # Article-related API endpoints
│   └── auth.py          # Authentication API endpoints
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd books-api
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   
   **Option 1: Use the setup script (Recommended)**
   ```bash
   python setup_env.py
   ```
   
   **Option 2: Manual setup**
   Copy the environment template and customize:
   ```bash
   cp env.example .env
   ```
   
   Then edit `.env` file with your settings:
   ```env
   SECRET_KEY=your-super-secret-key-change-this-in-production-123456789
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL=sqlite:///./books.db
   APP_NAME=Books & Articles API
   APP_VERSION=1.0.0
   CORS_ORIGINS=*
   ```

## Running the Application

1. **Start the development server:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the application:**
   - API: http://localhost:8000
   - Interactive API docs (Swagger UI): http://localhost:8000/docs
   - Alternative API docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register a new user | No |
| POST | `/api/v1/auth/login` | Login user and get access token | No |
| GET | `/api/v1/auth/me` | Get current user information | Yes |
| GET | `/api/v1/auth/users` | Get all users | Superuser only |
| GET | `/api/v1/auth/users/{user_id}` | Get specific user | Superuser only |

### Books

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/books/` | Get all books (with pagination and search) | No |
| POST | `/api/v1/books/` | Create a new book | Yes |
| GET | `/api/v1/books/{book_id}` | Get a specific book by ID | No |
| PUT | `/api/v1/books/{book_id}` | Update a book | Yes |
| DELETE | `/api/v1/books/{book_id}` | Delete a book | Yes |
| GET | `/api/v1/books/isbn/{isbn}` | Get a book by ISBN | No |

### Articles

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/articles/` | Get all articles (with pagination, search, and filters) | No |
| POST | `/api/v1/articles/` | Create a new article | Yes |
| GET | `/api/v1/articles/{article_id}` | Get a specific article by ID | No |
| PUT | `/api/v1/articles/{article_id}` | Update an article | Yes |
| DELETE | `/api/v1/articles/{article_id}` | Delete an article | Yes |
| GET | `/api/v1/articles/category/{category}` | Get articles by category | No |

### Other Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Root endpoint with API information | No |
| GET | `/health` | Health check endpoint | No |

## Example Usage

### Authentication

#### Register a New User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword123",
       "full_name": "John Doe"
     }'
```

**Note**: Passwords must be between 6-72 characters due to bcrypt limitations.

#### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=securepassword123"
```

#### Get Current User Info
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Books

#### Create a Book (Requires Authentication)
```bash
curl -X POST "http://localhost:8000/api/v1/books/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "The Great Gatsby",
       "author": "F. Scott Fitzgerald",
       "description": "A classic American novel",
       "isbn": "978-0-7432-7356-5",
       "price": 12.99,
       "publication_date": "1925-04-10T00:00:00"
     }'
```

#### Get All Books (Public)
```bash
curl "http://localhost:8000/api/v1/books/?skip=0&limit=10"
```

#### Search Books (Public)
```bash
curl "http://localhost:8000/api/v1/books/?search=gatsby"
```

#### Get Book by ID (Public)
```bash
curl "http://localhost:8000/api/v1/books/1"
```

#### Update a Book (Requires Authentication)
```bash
curl -X PUT "http://localhost:8000/api/v1/books/1" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "price": 15.99
     }'
```

#### Delete a Book (Requires Authentication)
```bash
curl -X DELETE "http://localhost:8000/api/v1/books/1" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Articles

#### Create an Article (Requires Authentication)
```bash
curl -X POST "http://localhost:8000/api/v1/articles/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Getting Started with FastAPI",
       "author": "John Doe",
       "content": "FastAPI is a modern web framework for building APIs with Python...",
       "summary": "Learn the basics of FastAPI development",
       "category": "Tutorial",
       "tags": "python,fastapi,web",
       "published": "published",
       "reading_time": 5
     }'
```

#### Get Articles with Filters (Public)
```bash
curl "http://localhost:8000/api/v1/articles/?category=Tutorial&published=published&search=FastAPI"
```

#### Get Articles by Category (Public)
```bash
curl "http://localhost:8000/api/v1/articles/category/Tutorial"
```

#### Update an Article (Requires Authentication)
```bash
curl -X PUT "http://localhost:8000/api/v1/articles/1" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "published": "published",
       "reading_time": 7
     }'
```

#### Delete an Article (Requires Authentication)
```bash
curl -X DELETE "http://localhost:8000/api/v1/articles/1" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database

The application uses SQLite database (`books.db`) which will be created automatically when you first run the application. The database file will be created in the project root directory.

### Database Schema

#### Books Table
The `books` table includes the following fields:
- `id`: Primary key (auto-increment)
- `title`: Book title (required, max 200 characters)
- `author`: Book author (required, max 100 characters)
- `description`: Book description (optional)
- `isbn`: ISBN number (optional, unique)
- `price`: Book price (optional, must be >= 0)
- `publication_date`: Publication date (optional)
- `created_at`: Record creation timestamp (auto-generated)
- `updated_at`: Record update timestamp (auto-generated)

#### Articles Table
The `articles` table includes the following fields:
- `id`: Primary key (auto-increment)
- `title`: Article title (required, max 200 characters)
- `author`: Article author (required, max 100 characters)
- `content`: Article content (required)
- `summary`: Article summary (optional)
- `category`: Article category (optional, max 50 characters)
- `tags`: Comma-separated tags (optional, max 500 characters)
- `published`: Publication status (draft, published, archived)
- `reading_time`: Reading time in minutes (optional, must be >= 1)
- `created_at`: Record creation timestamp (auto-generated)
- `updated_at`: Record update timestamp (auto-generated)

#### Users Table
The `users` table includes the following fields:
- `id`: Primary key (auto-increment)
- `username`: Username (required, unique, max 50 characters)
- `email`: Email address (required, unique, max 100 characters)
- `hashed_password`: Hashed password (required)
- `full_name`: Full name (optional, max 100 characters)
- `is_active`: Account status (default: true)
- `is_superuser`: Superuser status (default: false)
- `created_at`: Record creation timestamp (auto-generated)
- `updated_at`: Record update timestamp (auto-generated)

## Development

### Adding New Features

1. **Models**: Create new model files in `models/` directory
2. **Schemas**: Create new schema files in `schemas/` directory
3. **Routes**: Create new route files in `routes/` directory
4. **Database**: Update database configuration in `database.py` if needed
5. **Main App**: Import and include new routers in `main.py`

### Adding a New Resource

To add a new resource (e.g., "Authors"):

1. **Add Model**: Create `models/author.py` with the SQLAlchemy model
2. **Update Models Init**: Add the new model to `models/__init__.py`
3. **Add Schemas**: Create `schemas/author.py` with Pydantic schemas
4. **Update Schemas Init**: Add the new schemas to `schemas/__init__.py`
5. **Create Route File**: Create `routes/authors.py` with all endpoints
6. **Update Routes Init**: Add the new router to `routes/__init__.py`
7. **Update Main**: Import and include the router in `main.py`
8. **Add Authentication**: Protect endpoints using `get_current_active_user` dependency

### Authentication & Authorization

The API uses JWT (JSON Web Tokens) for authentication:

- **Registration**: Users can register with username, email, and password
- **Login**: Users receive a JWT token upon successful login
- **Token Expiration**: Tokens expire after 30 minutes (configurable)
- **Protected Endpoints**: Create, Update, Delete operations require authentication
- **Public Endpoints**: Read operations are publicly accessible
- **Superuser Access**: Some endpoints require superuser privileges
- **Password Security**: Passwords are hashed using bcrypt (max 72 characters)
- **Environment Configuration**: Configurable via environment variables

### Environment Variables

The application uses environment variables for configuration. All variables have sensible defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `your-secret-key-change-this-in-production` | JWT secret key (⚠️ **Change in production!**) |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time in minutes |
| `DATABASE_URL` | `sqlite:///./books.db` | Database connection URL |
| `APP_NAME` | `Books & Articles API` | Application name |
| `APP_VERSION` | `1.0.0` | Application version |
| `CORS_ORIGINS` | `*` | Allowed CORS origins (comma-separated) |

**Production Security Notes:**
- Always change `SECRET_KEY` to a secure random string
- Set `CORS_ORIGINS` to specific domains, not `*`
- Use a production database (PostgreSQL, MySQL) instead of SQLite
- Consider using environment-specific configurations

### Database Migrations

For production applications, consider using Alembic for database migrations:
```bash
pip install alembic
alembic init alembic
```

## Production Deployment

For production deployment:

1. **Environment Variables**: Use environment variables for database URLs and other sensitive data
2. **Database**: Consider using PostgreSQL or MySQL instead of SQLite
3. **Security**: Implement proper authentication and authorization
4. **CORS**: Configure CORS origins properly
5. **HTTPS**: Use HTTPS in production
6. **Process Manager**: Use a process manager like Gunicorn with Uvicorn workers

Example production command:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications
- **python-multipart**: For handling form data
- **python-jose[cryptography]**: JWT token handling
- **passlib[bcrypt]**: Password hashing and verification
- **python-dotenv**: Environment variable management

## License

This project is open source and available under the MIT License.
