# Clinic Management System

A production-oriented REST API for managing a medical clinic built with FastAPI.

The project demonstrates modern backend development practices including asynchronous programming, layered architecture, JWT authentication, RBAC/ABAC authorization, Repository Pattern, Unit of Work, Docker, Redis, Celery and comprehensive unit testing.

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy Async
- PostgreSQL
- Alembic
- Redis
- Celery
- Celery Beat
- Poetry
- Docker
- Pytest
- JWT
- Minio
- RabbitMQ
- Resend
- SlowAPI
- Jinja2

## Features

- Secure JWT authentication and authorization
- Fine-grained RBAC and ABAC access control
- Doctor, patient, and administrator management
- Appointment scheduling workflow
- Doctor availability management
- Electronic medical records
- Email notifications and account verification
- Background task processing with Celery
- Scheduled jobs with Celery Beat
- Object storage integration with MinIO
- Message broker powered by RabbitMQ
- API rate limiting
- Async PostgreSQL integration
- Database migrations with Alembic
- RESTful API with automatic Swagger documentation
- Docker-ready deployment
- 300+ unit tests with Pytest

## Project Structure

```text
clinic_management_system/
├── alembic/                 # Database migrations
├── src/
│   ├── app/
│   │   ├── appointments/    # Appointment management
│   │   ├── auth/            # Authentication & authorization
│   │   ├── medical_records/ # Medical records
│   │   ├── scheduling/      # Doctor schedules
│   │   └── users/           # User management
│   ├── common/              # Shared utilities
│   ├── core/                # Application configuration
│   ├── db/                  # Database configuration
│   ├── infrastructure/      # External integrations
│   └── main.py              # Application entry point
├── tests/                   # Unit tests
├── Dockerfile
├── docker-compose.yaml
├── pyproject.toml
└── README.md
```
## Architecture

The project is built as a feature-based modular monolith.

Each feature is isolated into its own module and contains all related components:

- API routers
- Services
- Repositories
- SQLAlchemy models
- Pydantic schemas
- Permissions
- Exceptions

Business logic is separated from the infrastructure layer using the Service Layer and Repository patterns. Database transactions are managed through the Unit of Work pattern, while authentication and authorization are implemented using JWT together with RBAC and ABAC policies.

## Getting Started

### Prerequisites

Before running the project, make sure you have installed:

- Python 3.12+
- Poetry
- Docker & Docker Compose

### Installation

```bash
git clone https://github.com/danilyukanton1-ship-it/clinic_management_system
cd clinic_management_system

poetry install
```

### Environment Variables

Create a `.env` file based on `.env.example` and configure:

- PostgreSQL
- RabbitMQ
- Redis
- MinIO
- Resend
- JWT

### Start Services

Build and start all application services:

```bash
docker compose up -d --build
```

This command starts:

- FastAPI application
- PostgreSQL
- Redis
- RabbitMQ
- MinIO
- Celery Worker
- Celery Beat

### Apply Database Migrations

```bash
docker compose exec app alembic upgrade head
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

```bash
pytest
```