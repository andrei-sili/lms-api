# LMS API

REST API for a Learning Management System, built with Django and Django REST Framework:
courses, lessons, quizzes, enrollments, certificates and subscriptions, secured with JWT
authentication and role-based access control (student, teacher, admin).

## Features

- **JWT authentication** (obtain, refresh, verify) with a custom user model: login by
  e-mail, roles `student`, `teacher`, `admin`, plus password-reset tokens
- **Courses** with categories, enrollments (status lifecycle) and completion certificates
- **Lessons** with file attachments, comments and per-user progress tracking
- **Quizzes** with questions, answers and user attempts
- **Subscriptions** that gate access to paid content
- **Role-based permissions**: teachers can only manage their own courses, admin-only
  resources, read access for authenticated users
- **Filtering and pagination** on list endpoints (django-filter, 10 items per page);
  every endpoint requires authentication by default

## Tech stack

Python · Django 5.2 · Django REST Framework 3.16 · SimpleJWT · django-filter ·
SQLite (development) / PostgreSQL (production)

## API overview

| Prefix | Resources |
|---|---|
| `/api/auth/token/` | JWT obtain / `refresh/` / `verify/` |
| `/api/users/` | user accounts |
| `/api/courses/` | courses, `categories/`, `course_categories/`, `enrollments/`, `certificates/` |
| `/api/lessons/` | lessons, `attachments/`, `comments/`, `progress/` |
| `/api/quizzes/` | quizzes, `questions/`, `answers/`, `attempts/` |
| `/api/subscriptions/` | subscriptions |

## Getting started

Requires Python 3.12+.

```bash
git clone https://github.com/andrei-sili/lms-api && cd lms-api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

echo "DJANGO_SECRET_KEY=change-me" > .env   # required

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The settings are split per environment (`lms_api/settings/`): `ENV=development`
(default) runs on SQLite, `ENV=production` reads a PostgreSQL configuration from the
environment (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, ...). A Makefile
wraps the common commands: `make run`, `make migrate`, `make superuser`.

## Project structure

```
apps/
  users/          custom user model, roles, password reset
  courses/        courses, categories, enrollments, certificates
  lessons/        lessons, attachments, comments, progress
  quizzes/        quizzes, questions, answers, attempts
  subscriptions/  subscription plans and access
lms_api/
  settings/       base / development / production
```

## License

[MIT](LICENSE)
