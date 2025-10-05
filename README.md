# Books & Articles API

A FastAPI application for managing books and articles with SQLite database using SQLAlchemy, featuring JWT authentication and authorization.

## Features

### 🚀 Core API Features
- **CRUD Operations**: Complete Create, Read, Update, Delete for books and articles
- **Advanced Search**: Full-text search across titles, authors, and content
- **Smart Filtering**: Filter articles by category and publication status
- **Pagination**: Efficient data pagination for large datasets
- **ISBN Support**: Unique ISBN validation for books

### 🔐 Security & Authentication
- **JWT Authentication**: Secure token-based authentication system
- **Google OAuth2**: Sign in with Google accounts
- **Dual Authentication**: Both email/password and Google OAuth2 support
- **Role-based Authorization**: Different access levels for regular users and superusers
- **User Management**: Registration, login, and profile management
- **Password Security**: bcrypt hashing with automatic length validation
- **Protected Endpoints**: Create/Update/Delete operations require authentication

### 🏗️ Architecture & Development
- **Modular Architecture**: Organized route, model, and schema structure for scalability
- **Data Validation**: Pydantic models for comprehensive request/response validation
- **Auto Documentation**: Interactive API docs with Swagger UI and ReDoc
- **Environment Configuration**: Configurable via environment variables
- **Automated Setup**: One-command setup with secure key generation

### 🗄️ Database & Performance
- **SQLite Database**: Lightweight, serverless database (easily upgradeable)
- **SQLAlchemy ORM**: Robust object-relational mapping
- **Database Migrations**: Ready for production database migrations
- **Connection Pooling**: Efficient database connection management

## Project Structure

```
books-api/
├── main.py              # FastAPI application entry point
├── auth.py              # JWT authentication utilities
├── database.py          # Database configuration and connection
├── setup_env.py         # Environment setup script
├── env.example          # Environment variables template
├── .env                 # Environment variables (auto-generated)
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
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Quick Start

### 🚀 Automated Setup (Recommended)

1. **Clone or navigate to the project directory:**
   ```bash
   cd books-api
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   python setup_env.py
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

6. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

### ✨ Setup Script Features

The `setup_env.py` script automatically:
- 🔑 **Generates secure secret keys** - Creates cryptographically secure JWT secrets
- 📝 **Creates .env file** - Sets up environment configuration
- ⚙️ **Configures defaults** - Uses production-ready settings
- 🛡️ **Security first** - Ensures secure defaults for development

## Manual Installation

If you prefer manual setup:

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
| POST | `/api/v1/auth/login` | Login user (OAuth2 form - username field = email) | No |
| POST | `/api/v1/auth/login-email` | Login user with email (JSON format) | No |
| GET | `/api/v1/auth/google/login` | Initiate Google OAuth2 login | No |
| GET | `/api/v1/auth/google/callback` | Google OAuth2 callback | No |
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

### 🔍 Query Parameters

#### Books & Articles List Endpoints
- `page`: Page number (default: 1)
- `size`: Items per page (default: 10, max: 100)
- `search`: Search term for titles, authors, and content
- `sort`: Sort field (title, author, created_at, etc.)
- `order`: Sort order (asc, desc)

#### Articles Additional Filters
- `category`: Filter by article category
- `published`: Filter by publication status (draft, published, archived)

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
     -d "email=user@example.com&password=securepassword123"
```

#### Login User (Email-based JSON - Recommended)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login-email" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "securepassword123"
     }'
```

#### Get Current User Info
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Google OAuth2 Login
```bash
# Step 1: Get Google authorization URL
curl -X GET "http://localhost:8000/api/v1/auth/google/login"

# Response:
# {
#   "authorization_url": "https://accounts.google.com/o/oauth2/auth?...",
#   "state": "random_state_string"
# }

# Step 2: User visits the authorization_url in browser
# Step 3: Google redirects to callback with authorization code
# Step 4: The callback endpoint handles the code and returns JWT token
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

- **Registration**: Users can register with email, and password
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
| `GOOGLE_CLIENT_ID` | - | Google OAuth2 client ID |
| `GOOGLE_CLIENT_SECRET` | - | Google OAuth2 client secret |
| `GOOGLE_REDIRECT_URI` | `http://localhost:8000/api/v1/auth/google/callback` | Google OAuth2 redirect URI |

**Production Security Notes:**
- Always change `SECRET_KEY` to a secure random string
- Set `CORS_ORIGINS` to specific domains, not `*`
- Use a production database (PostgreSQL, MySQL) instead of SQLite
- Consider using environment-specific configurations

### Google OAuth2 Setup

To enable Google OAuth2 authentication:

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select an existing one
3. **Enable Google+ API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it
4. **Create OAuth2 credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - Development: `http://localhost:8000/api/v1/auth/google/callback`
     - Production: `https://yourdomain.com/api/v1/auth/google/callback`
5. **Update your `.env` file**:
   ```env
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
   ```

### Database Migrations

For production applications, consider using Alembic for database migrations:
```bash
pip install alembic
alembic init alembic
```

## Troubleshooting

### Common Issues

#### 🔧 Port Already in Use
```bash
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```
**Solution:** Kill existing processes or use a different port:
```bash
pkill -f "python main.py"
# Or run on different port:
uvicorn main:app --port 8001
```

#### 🔐 Authentication Issues
- **Password too long**: Ensure passwords are ≤72 characters (bcrypt limitation)
- **Invalid token**: Check if token is expired (default: 30 minutes)
- **User not found**: Verify email exists in database

#### 📦 Dependency Issues
```bash
# If you get import errors, reinstall dependencies:
pip install -r requirements.txt --force-reinstall
```

#### 🗄️ Database Issues
- **Database locked**: Ensure no other processes are using the database
- **Migration needed**: Delete `books.db` to recreate tables with latest schema

### Getting Help

1. **Check the logs** - Look for error messages in the terminal
2. **Verify environment** - Ensure `.env` file exists and is properly configured
3. **Test endpoints** - Use the interactive docs at `/docs` to test API endpoints
4. **Check dependencies** - Ensure all packages are installed correctly

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

## Contributing

We welcome contributions! Here's how to get started:

### 🚀 Development Setup

1. **Fork the repository** and clone your fork
2. **Set up development environment:**
   ```bash
   git clone <your-fork-url>
   cd books-api
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python setup_env.py
   ```

3. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes** following the existing code structure
5. **Test your changes:**
   ```bash
   python main.py
   # Test endpoints at http://localhost:8000/docs
   ```

6. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature-name
   ```

7. **Submit a pull request** with a clear description

### 📋 Development Guidelines

- **Code Style**: Follow existing patterns and structure
- **Documentation**: Update README for new features
- **Testing**: Test all endpoints manually or add automated tests
- **Security**: Ensure authentication/authorization is properly implemented
- **Environment**: Use environment variables for configuration

### 🐛 Reporting Issues

When reporting issues, please include:
- **Environment details** (OS, Python version)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and logs
- **Screenshots** if applicable

## License

This project is open source and available under the MIT License.
