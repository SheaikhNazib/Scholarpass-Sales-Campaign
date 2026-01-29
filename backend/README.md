# ScholarPASS Backend

A modern, scalable backend API built with FastAPI, PostgreSQL, Redis, and Docker.

## Architecture

- **Framework**: FastAPI (async Python web framework)
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **Cache**: Redis 7
- **Migrations**: Alembic with auto-generation
- **Containerization**: Docker & Docker Compose
- **Architecture Pattern**: Hexagonal Architecture (Ports & Adapters)

## Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Make (for running commands)

## Quick Start

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env if needed (defaults work for local development)
```

### 2. Start Services

```bash
# Start all services (PostgreSQL, Redis, FastAPI)
make up

# View logs
make logs

# Check health
make health
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

### 3. Run Migrations

```bash
# Run pending migrations
make migrate

# Create a new migration
make migration msg="Add users table"
```

## Available Commands

### Service Management

```bash
make up                    # Start all services
make down                  # Stop all services
make down-volumes          # Stop and remove volumes (clean slate)
make build                 # Build Docker images
make health                # Check service health
```

### Database Migrations

```bash
make migration msg="..."   # Create new migration with auto-generation
make migrate               # Run pending migrations
make db-reset              # Reset database (drops all data)
make db-seed               # Seed database with sample data
```

### Development

```bash
make logs                  # View app logs
make logs-db               # View database logs
make logs-redis            # View Redis logs
make shell                 # Open Python shell
make db-shell              # Open PostgreSQL shell
make redis-cli             # Open Redis CLI
make clean                 # Clean up containers and cache
```

### Code Quality

```bash
make lint                  # Run linting (flake8)
make format                # Format code (black)
make test                  # Run tests
make test-coverage         # Run tests with coverage report
```

### Production

```bash
make prod-build            # Build production image
make prod-up               # Start production services
make prod-down             # Stop production services
```

## Environment Variables

Key environment variables in `.env`:

```env
# Database
DATABASE_URL=postgresql://scholarpass_user:scholarpass_password@db:5432/scholarpass_db
DATABASE_ECHO=False

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Application
PORT=8000
DEBUG=True
ENVIRONMENT=development

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

## Project Structure

```
backend/
├── src/
│   ├── infrastructure/
│   │   ├── database.py      # SQLAlchemy setup
│   │   ├── redis.py         # Redis client
│   │   ├── auth.py          # Authentication
│   │   ├── security.py      # Security utilities
│   │   └── exceptions.py    # Custom exceptions
│   ├── modules/             # Feature modules (hexagonal architecture)
│   │   ├── user/
│   │   ├── access/
│   │   ├── notification/
│   │   └── ...
│   ├── config.py            # Configuration
│   └── main.py              # FastAPI app entry point
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files
│   ├── env.py               # Alembic environment
│   └── script.py.mako       # Migration template
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker Compose configuration
├── Makefile                 # Make commands
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (local)
├── .env.example             # Environment template
└── README.md                # This file
```

## Database Migrations

### Creating Migrations

Alembic auto-generates migrations based on your SQLAlchemy models:

```bash
# Create a new migration
make migration msg="Add users table"

# This will:
# 1. Compare current models with database schema
# 2. Generate migration file in alembic/versions/
# 3. You can review and edit if needed
```

### Running Migrations

```bash
# Run all pending migrations
make migrate

# Or manually:
docker-compose exec app alembic upgrade head

# View migration history
docker-compose exec app alembic history
```

### Downgrading

```bash
# Downgrade one migration
docker-compose exec app alembic downgrade -1

# Downgrade to specific revision
docker-compose exec app alembic downgrade <revision_id>
```

## Adding Models

1. Create your model in the appropriate module:

```python
# src/modules/user/models.py
from sqlalchemy import Column, Integer, String
from src.infrastructure.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
```

2. Import the model in `alembic/env.py` (already configured)

3. Create migration:

```bash
make migration msg="Add users table"
```

4. Review and run:

```bash
make migrate
```

## Redis Usage

```python
from src.infrastructure.redis import get_redis_client, set_cached, get_cached

# Get Redis client
redis = get_redis_client()

# Set cache
await set_cached("user:1", user_data, ttl=3600)

# Get cache
user = await get_cached("user:1")

# Delete cache
await delete_cached("user:1")
```

## Debugging

### View Logs

```bash
# Application logs
make logs

# Database logs
make logs-db

# Redis logs
make logs-redis

# All logs
docker-compose logs -f
```

### Database Shell

```bash
make db-shell

# Then run SQL queries
SELECT * FROM users;
```

### Redis CLI

```bash
make redis-cli

# Then run Redis commands
KEYS *
GET user:1
```

### Python Shell

```bash
make shell

# Then interact with app
from src.infrastructure.database import SessionLocal
db = SessionLocal()
# ... your code
```

## Troubleshooting

### Services won't start

```bash
# Check Docker is running
docker ps

# View detailed logs
docker-compose logs

# Rebuild images
make build
make up
```

### Database connection errors

```bash
# Check database is healthy
docker-compose ps

# View database logs
make logs-db

# Reset database
make db-reset
```

### Port already in use

```bash
# Find process using port
lsof -i :8000
lsof -i :5432
lsof -i :6379

# Kill process
kill -9 <PID>
```

### Migrations failing

```bash
# Check migration history
docker-compose exec app alembic history

# View current database version
docker-compose exec app alembic current

# Check for conflicts
docker-compose exec app alembic branches
```

## Development Workflow

1. **Start services**:
   ```bash
   make up
   ```

2. **Create/modify models** in `src/modules/*/models.py`

3. **Generate migration**:
   ```bash
   make migration msg="Your description"
   ```

4. **Review migration** in `alembic/versions/`

5. **Run migration**:
   ```bash
   make migrate
   ```

6. **Develop features** (hot reload enabled)

7. **Test changes**:
   ```bash
   make test
   ```

8. **Format code**:
   ```bash
   make format
   ```

## Production Deployment

### Build Production Image

```bash
make prod-build
```

### Environment Setup

Create `.env.production`:

```env
DATABASE_URL=postgresql://user:password@prod-db:5432/scholarpass_db
REDIS_URL=redis://prod-redis:6379/0
JWT_SECRET=<strong-random-secret>
DEBUG=False
ENVIRONMENT=production
```

### Deploy

```bash
make prod-up
```

## Performance Tips

1. **Database**: Use connection pooling (configured)
2. **Redis**: Cache frequently accessed data
3. **API**: Use async/await for I/O operations
4. **Queries**: Use eager loading to avoid N+1 queries
5. **Indexes**: Add database indexes for frequently queried columns

## Security

- Change `JWT_SECRET` in production
- Use strong database passwords
- Enable HTTPS in production
- Validate all inputs
- Use environment variables for secrets
- Keep dependencies updated

## Contributing

1. Create feature branch
2. Make changes
3. Run tests: `make test`
4. Format code: `make format`
5. Commit and push
6. Create pull request

## Support

For issues or questions, check:
- Docker logs: `make logs`
- Database logs: `make logs-db`
- Redis logs: `make logs-redis`
- API docs: http://localhost:8000/docs

## License

Proprietary - ScholarPASS
