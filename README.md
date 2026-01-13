# BE Capstone – Document Editor API

A Django REST API that allows users to create projects, edit documents, and track document version history.

---

## Tech Stack
- Python
- Django
- Django REST Framework
- JWT Authentication (SimpleJWT)
- SQLite (development)

---

## Features
- User registration and login (JWT)
- Create, update, and delete projects
- One document per project
- Auto-save document content
- Document version history tracking
- Access restricted to project owner

---

## API Endpoints

### Auth
- POST /api/auth/register/
- POST /api/auth/login/

### Projects
- GET /api/projects/
- POST /api/projects/
- PUT /api/projects/:id/
- DELETE /api/projects/:id/

### Documents
- GET /api/projects/:id/document/
- PUT /api/projects/:id/document/

### History
- GET /api/document/:id/history/

---

## Setup Instructions

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
