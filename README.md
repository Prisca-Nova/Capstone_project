DocFlow - Modern Document Editor API
https://img.shields.io/badge/DocFlow-Document%2520Editor-blue
https://img.shields.io/badge/Django-5.0.6-green
https://img.shields.io/badge/DRF-3.15.1-red
https://img.shields.io/badge/JWT-Auth-orange

A full-featured document editor and management system built with Django REST Framework. Features include real-time editing, version history, AI-powered writing assistance, and a modern responsive interface.

✨ Features
🔐 Authentication & Security
JWT-based authentication (register/login/refresh)

Secure password hashing with validation

Role-based access control

Session management

📁 Project Management
Create, read, update, and delete projects

One project = One document (with auto-creation)

Project descriptions and metadata

Search and filter projects

✏️ Document Editing
Rich text editor with markdown support

Auto-save functionality (every 30 seconds)

Real-time word and character count

Text formatting (bold, italic, headings, lists)

Export to multiple formats (TXT, HTML, Markdown)

🕰️ Version History
Automatic snapshot creation on each save

Version restoration capabilities

History timeline with previews

Compare different versions

🤖 AI Writing Assistant
Text summarization

Writing improvement suggestions

Idea generation

Grammar checking

📊 Analytics & Dashboard
User statistics (projects, words, edits)

Writing productivity metrics

Recent activity tracking

Visual progress indicators

🎨 Modern UI/UX
Dark/Light theme toggle

Responsive design (mobile & desktop)

Glass-morphism design elements

Smooth animations and transitions

Toast notifications

Loading states

🛠️ Tech Stack
Backend
Python 3.10+

Django 5.0.6 - Web framework

Django REST Framework 3.15.1 - API framework

djangorestframework-simplejwt 5.3.1 - JWT authentication

PostgreSQL/SQLite - Database

django-cors-headers - CORS support

Frontend
HTML5/CSS3 - Structure and styling

JavaScript (ES6+) - Interactivity

Tailwind CSS - Utility-first CSS framework

Font Awesome - Icons

Inter Font - Modern typography

🚀 Quick Start
Prerequisites
Python 3.10 or higher

pip (Python package manager)

Virtual environment (recommended)

Installation
Clone the repository

bash
git clone <repository-url>
cd capstone_project/core
Create and activate virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Configure environment variables

bash
# Create .env file
echo "SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3" > .env
Run migrations

bash
python manage.py makemigrations
python manage.py migrate
Create superuser (optional)

bash
python manage.py createsuperuser
Run development server

bash
python manage.py runserver
The application will be available at:

Frontend: http://localhost:8000

Admin Panel: http://localhost:8000/admin

API Base: http://localhost:8000/api

📁 Project Structure
text
capstone_project/
├── core/
│   ├── api/                          # Main application
│   │   ├── __init__.py
│   │   ├── admin.py                  # Admin configurations
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── serializers.py            # API serializers
│   │   ├── views.py                  # API views
│   │   ├── urls.py                   # API routes
│   │   ├── permissions.py            # Custom permissions
│   │   └── ai_services.py            # AI functionalities
│   │
│   ├── core/                         # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py               # Project settings
│   │   ├── urls.py                   # Project URLs
│   │   ├── wsgi.py                   # WSGI configuration
│   │   └── asgi.py                   # ASGI configuration
│   │
│   ├── templates/                    # HTML templates
│   │   └── index.html                # Main frontend
│   │
│   ├── static/                       # Static files (CSS, JS, images)
│   ├── media/                        # User uploaded files
│   │
│   ├── manage.py                     # Django management script
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables
│   └── db.sqlite3                    # Database (development)
🔧 API Endpoints
Authentication
Method	Endpoint	Description
POST	/api/auth/register/	Register new user
POST	/api/auth/login/	Login user (get tokens)
POST	/api/auth/refresh/	Refresh JWT token
Projects
Method	Endpoint	Description
GET	/api/projects/	List all user projects
POST	/api/projects/	Create new project
GET	/api/projects/{id}/	Get project details
PUT	/api/projects/{id}/	Update project
DELETE	/api/projects/{id}/	Delete project
GET	/api/projects/{id}/document/	Get project document
PUT	/api/projects/{id}/document/	Update document content
GET	/api/projects/{id}/stats/	Get project statistics
Documents
Method	Endpoint	Description
GET	/api/documents/{id}/history/	Get document history
GET	/api/documents/{id}/history/recent/	Get recent history
User & Analytics
Method	Endpoint	Description
GET	/api/user/profile/	Get user profile
PUT	/api/user/profile/	Update user profile
GET	/api/analytics/	Get user analytics
AI Tools
Method	Endpoint	Description
POST	/api/ai/summarize/	Summarize text
POST	/api/ai/improve/	Get writing suggestions
POST	/api/ai/ideas/	Generate topic ideas
🗄️ Database Models
User
Custom user model extending AbstractUser

Email as primary identifier

Additional fields: created_at, username

Project
Belongs to a User (owner)

Fields: title, description, created_at

Auto-creates a Document when created

Document
One-to-one relationship with Project

Fields: content, last_modified

Auto-saves to History on updates

History
Tracks document version history

Fields: content_snapshot, timestamp

ForeignKey to Document

🔐 Authentication Flow
text
1. User registers → POST /api/auth/register/
   ↓
2. Receives JWT tokens (access & refresh)
   ↓
3. Uses access token for authenticated requests
   ↓
4. Token expires → POST /api/auth/refresh/
   ↓
5. Gets new access token
🎨 Frontend Features
Dashboard
Overview of all projects

Writing statistics

Recent activity

Quick actions

Editor
Real-time text editing

Formatting toolbar

Word/character counter

Auto-save indicator

Version history sidebar

Projects View
Grid/list view of projects

Search and filter

Create new projects

Project statistics

Responsive Design
Mobile-friendly navigation

Adaptive layouts

Touch-friendly controls

Optimized for all screen sizes

⚙️ Configuration
Environment Variables
Create a .env file in the project root:

env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# For production (optional)
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
Settings Customization
Key settings in core/settings.py:

python
# Security
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3')
    )
}

# CORS (for development)
CORS_ALLOW_ALL_ORIGINS = True

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
🧪 Testing
Run Tests
bash
python manage.py test api
API Testing with cURL
bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "testuser", "password": "testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Create Project (with token)
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Project", "description": "Test project"}'
Postman Collection
Import the following to Postman:

json
{
  "info": {
    "name": "DocFlow API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/auth/register/",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"username\": \"testuser\",\n  \"password\": \"testpass123\"\n}"
            }
          }
        }
      ]
    }
  ]
}
🚀 Deployment
Deploy to Heroku
bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
Deploy to PythonAnywhere
Upload project files

Create virtual environment

Install requirements

Configure WSGI file

Set up static files

Run migrations

Docker Deployment
dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
bash
# Build and run
docker build -t docflow .
docker run -p 8000:8000 docflow
📈 Performance Optimization
Database Indexing
python
# Add to models for better performance
class Meta:
    indexes = [
        models.Index(fields=['owner', 'created_at']),
        models.Index(fields=['last_modified']),
    ]
Caching
python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    }
}
Pagination
All list endpoints support pagination:

?page=2

?page_size=50

🔍 Troubleshooting
Common Issues
Migration Errors

bash
# Reset migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
python manage.py makemigrations
python manage.py migrate
Static Files Not Loading

bash
python manage.py collectstatic
CORS Errors

python
# In settings.py
CORS_ALLOW_ALL_ORIGINS = True  # For development
# OR for production
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
Database Issues

bash
# Recreate database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
Debug Mode
Set DEBUG = True in .env to see detailed error messages.

📚 API Documentation
Request/Response Examples
Register User:

json
// Request
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123"
}

// Response (201 Created)
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "john_doe"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "message": "Registration successful!"
}
Create Project:

json
// Request
{
  "title": "My Research Paper",
  "description": "Research on climate change effects"
}

// Response (201 Created)
{
  "id": 1,
  "owner": "user@example.com",
  "title": "My Research Paper",
  "description": "Research on climate change effects",
  "created_at": "2024-01-15T10:30:00Z",
  "document_count": 0,
  "last_modified": null
}
🤝 Contributing
Fork the repository

Create a feature branch

Make your changes

Write tests

Submit a pull request

Development Setup
bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Check code style
flake8 .

# Run with debug mode
DEBUG=True python manage.py runserver
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👏 Acknowledgments
Django and Django REST Framework teams

Tailwind CSS for the awesome styling framework

Font Awesome for icons

All contributors and testers

📞 Support
For support, please:

Check the troubleshooting section

Search existing issues

Create a new issue with detailed information

Built with ❤️ for the ALX Capstone Project

Happy Document Editing! 📝✨