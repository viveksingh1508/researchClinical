# Clinical Research Platform API

A lightweight REST API for managing clinical research studies, sites, users, and subject data submissions.

## Features

- **Study Management**: Create and manage research studies
- **Site Management**: Create sites and assign them to studies
- **User Management**: Handle administrators and research subjects
- **Subject Assignments**: Assign subjects to specific sites
- **Data Collection**: Enable subjects to upload data to their assigned sites
- **OpenAPI 3.0**: Interactive API documentation with Swagger UI
- **PostgreSQL**: Reliable data persistence
- **Docker**: Fully containerized setup

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **API Documentation**: drf-spectacular (OpenAPI 3.0)
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd clinical_research_api
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - API Base URL: http://localhost:8000/api/
   - Swagger UI: http://localhost:8000/api/docs/
   - OpenAPI Schema: http://localhost:8000/api/schema/
   - Django Admin: http://localhost:8000/admin/

4. **Create a superuser (optional)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## API Endpoints

### Core Resources

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/users/` | GET, POST, PUT, DELETE | User management |
| `/api/studies/` | GET, POST, PUT, DELETE | Study management |
| `/api/sites/` | GET, POST, PUT, DELETE | Site management |
| `/api/assignments/` | GET, POST, PUT, DELETE | Subject-to-site assignments |
| `/api/subject-data/` | GET, POST, PUT, DELETE | Subject data uploads |

### Special Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/studies/{id}/subjects/` | GET | List all subjects in a study |
| `/api/sites/{id}/subjects/` | GET | List subjects assigned to a site |
| `/api/sites/{id}/subject_data/` | GET | View all data uploaded to a site |

## Example Usage

### 1. Create an Administrator
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "first_name": "vivek",
    "last_name": "Admin",
    "email": "vivek@example.com",
    "role": "admin",
    "password": "securepassword"
  }'
```

### 2. Create a Study
```bash
curl -X POST http://localhost:8000/api/studies/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-encoded-credentials>" \
  -d '{
    "name": "COVID-19 Vaccine Trial",
    "description": "Phase 3 clinical trial for COVID-19 vaccine",
    "administrator_ids": [1]
  }'
```

### 3. Create a Site
```bash
curl -X POST http://localhost:8000/api/sites/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-encoded-credentials>" \
  -d '{
    "name": "Test Clinic - New Delhi",
    "location": "New Delhi, INDIA",
    "study": 1
  }'
```

### 4. Create a Subject
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-encoded-credentials>" \
  -d '{
    "username": "subject1",
    "first_name": "vivek",
    "last_name": "singh",
    "email": "vivek@example.com",
    "role": "subject",
    "password": "subjectpassword"
  }'
```

### 5. Assign Subject to Site
```bash
curl -X POST http://localhost:8000/api/assignments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-encoded-credentials>" \
  -d '{
    "subject": 2,
    "site": 1
  }'
```

### 6. Subject Uploads Data
```bash
curl -X POST http://localhost:8000/api/subject-data/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-encoded-credentials>" \
  -d '{
    "subject_name": "Subject 1",
    "data": {"temperature": 98.6, "heart_rate": 72, "blood_pressure": "120/80"},
    "site": 1
  }'
```

## Data Models

### User
- Custom user model extending Django's AbstractUser
- Fields: username, first_name, last_name, email, role (admin/subject)
- Role-based permissions for API access

### Study
- Fields: name, description, created_at
- Many-to-many relationship with administrators

### Site
- Fields: name, location, created_at
- Foreign key to Study

### SubjectAssignment
- Links subjects to sites
- Unique constraint prevents duplicate assignments

### SubjectData
- Fields: subject_name, data (JSON), uploaded_at
- Foreign keys to Site and uploader (User)

## Authentication

The API uses Django's built-in session authentication and basic authentication. For production use, consider implementing JWT tokens or OAuth2.

## Permissions

- **Administrators**: Full CRUD access to all resources
- **Subjects**: Can only upload data to their assigned sites and view their own data
- **Anonymous**: No access (authentication required)

## Development

### Running Tests
```bash
docker-compose exec web python manage.py test
```

### Making Database Changes
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Accessing Django Shell
```bash
docker-compose exec web python manage.py shell
```

## Design Notes

1. **Role-based Access**: Simple admin/subject role system handles permissions
2. **Flexible Data Storage**: JSON field allows various data formats for subject submissions
3. **Site-based Organization**: Studies contain sites, subjects are assigned to specific sites
4. **Audit Trail**: Timestamps track when data is created/uploaded
5. **Docker-first**: Entire application runs in containers for consistency

## Environment Variables

Create a `.env` file to customize database settings:

```env
DB_NAME=clinical_research
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DEBUG=True
```

## Production Considerations

For production deployment:

1. Set `DEBUG=False`
2. Configure secure `SECRET_KEY`
3. Add proper `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Implement proper authentication (JWT/OAuth2)
6. Add rate limiting and API throttling
7. Configure HTTPS
8. Set up database backups
9. Add logging and monitoring