# Learn Chinese Final Project

Learn Chinese is a full-stack web application for practical Chinese learning. It uses Django Templates for the frontend, Django REST Framework for APIs, Django Admin for content management, PostgreSQL for production data, Redis for caching/sessions, and Nginx as the frontend reverse proxy.

The business model is a simulated premium subscription: free users can access open courses, while premium users unlock advanced course content. Premium status is managed in Django Admin.

## Features

- User registration, login, logout, and secure Django password hashing.
- Role-based admin access through Django Admin.
- Admin-managed learning goals, courses, lessons, quizzes, questions, and answers.
- Free vs premium course access.
- DRF API endpoints under `/api/`.
- OpenAPI schema at `/api/schema/` and Swagger UI at `/api/schema/swagger-ui/`.
- Redis-backed cache and sessions in Docker.
- Structured console logging.
- Multi-service Docker setup with frontend, backend, database, and Redis.

## Run with Docker

Copy the example environment file if you want to customize values:

```bash
cp .env.example .env
```

Start the whole application with one command:

```bash
docker compose up -d --build
```

Open:

- Frontend/Nginx: `http://localhost/`
- Backend direct port: `http://localhost:8000/`
- Admin: `http://localhost/admin/`
- API schema: `http://localhost/api/schema/`

Create an admin user:

```bash
docker compose exec backend python manage.py createsuperuser
```

Stop the application:

```bash
docker compose down
```

## Local Development

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run migrations and start Django:

```bash
python manage.py migrate
python manage.py runserver
```

Without PostgreSQL environment variables, the app falls back to local SQLite. Without `REDIS_URL`, it falls back to local memory cache.

## Testing

```bash
python manage.py check
python manage.py test
```

The test suite covers public page rendering, registration, login, logout, API access, and premium course locking behavior.

## Caching and Logging

In Docker, the cache and user sessions use Redis through `REDIS_URL=redis://redis:6379/1`. Locally, if Redis is not configured, Django uses an in-memory cache so development remains simple.

Logs are written to stdout with timestamps, logger name, level, and message. The log level is controlled by `LOG_LEVEL`.

## Premium Demo Flow

1. Register a normal user from `/signup/`.
2. Create or edit a course in `/admin/` and mark `is_premium=True`.
3. Visit `/course/` as the normal user and confirm the premium course is locked.
4. In Django Admin, edit the user and set `is_premium=True`.
5. Return to `/course/` and confirm the course lessons are visible.
