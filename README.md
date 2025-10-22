# 🌌 Planetarium API Service

A robust Django REST Framework-based API for managing planetarium content, shows, sessions, and reservations.  
The project is fully containerized with Docker and secured using JWT authentication for safe and reliable access.

## 🌟 Features

- **JWT Authentication** using `djangorestframework-simplejwt`
- **Core Models:**
    - `Themes`
    - `Domes`
    - `Shows`
    - `Sessions`
    - `Reservations`
- **Interactive API Documentation** with `drf-spectacular` (Swagger UI & Redoc)
- **Dockerized Setup** for easy development & deployment
- **Customizable Access Restrictions**
- **Environment Variable Configuration** via `.env`

## 🛠️ Tech Stack

- **Python:** 3.11+
- **Web Framework:** Django & Django REST Framework
- **Database:** PostgreSQL (via Docker)
- **Containerization:** Docker & Docker Compose
- **Authentication:** JWT
- **API Documentation:** `drf-spectacular`

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.11+](https://www.python.org/downloads/)

### Local Setup (without Docker)

```bash
git clone https://github.com/Andreyome/Planetarium-API-Service.git
cd Planetarium-API-Service

python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create .env file:
POSTGRES_PASSWORD=<PASSWORD>
POSTGRES_USER=<USER>
POSTGRES_DB=<DATABASE>
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your_secret_key_for_django
PGDATA=/var/lib/postgresql/data

**Apply database migrations and start the development server:**

```bash
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### Docker Setup

```bash
docker compose build
docker compose up
```

To stop and remove containers:

```bash
docker compose down
```

## 🔐 Authentication & Access

This API uses JWT authentication.

| Endpoint                   | Method | Description                                |
|----------------------------|--------|--------------------------------------------|
| `/api/user/register/`      | `POST` | Register a new user                        |
| `/api/user/token/`         | `POST` | Obtain access & refresh tokens             |
| `/api/user/token/refresh/` | `POST` | Refresh an expired access token            |
| `/api/user/me/`            | `GET`  | Retrieve current user profile              |
| `/api/user/token/verify/`  | `POST` | Takes a token and indicates if it is valid |

**Using Tokens:**  
Add to request headers:

```
Authorization: Bearer <your_access_token>
```

## 📄 API Documentation

Available after running the project:

- **Swagger UI:** `http://127.0.0.1:8000/api/doc/swagger/`
- **Redoc:** `http://127.0.0.1:8000/api/doc/redoc/`

## 🌐 API Endpoints Overview

| Endpoint                         | Method   | Description                                  |
|----------------------------------|----------|----------------------------------------------|
| `/api/planetarium/themes/`       | GET/POST | List all themes / Create a new theme         |
| `/api/planetarium/domes/`        | GET/POST | List all domes / Create a new dome           |
| `/api/planetarium/shows/`        | GET/POST | List all shows / Create a new show           |
| `/api/planetarium/sessions/`     | GET/POST | List all sessions / Create a new session     |
| `/api/planetarium/reservations/` | GET/POST | List all reservations / Create a reservation |

## 🤝 Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m "Add YourFeature"`
4. Push: `git push origin feature/YourFeature`
5. Open a Pull Request

---
