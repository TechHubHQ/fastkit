# Generated Project Structure by FastKit

This document shows what the directory structure looks like for projects created using FastKit CLI commands.

## 🚀 Basic Project: `fastkit new my-project`

When a user runs `fastkit new my-project`, here's the initial structure that gets generated:

```
my-project/
├── 📱 Application Core
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI application instance
│   │   ├── api/                     # API routes
│   │   │   ├── __init__.py
│   │   │   ├── deps.py              # Common dependencies
│   │   │   └── v1/                  # API version 1
│   │   │       ├── __init__.py
│   │   │       └── api.py           # Main API router
│   │   ├── core/                    # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # Application settings
│   │   │   ├── security.py          # Security utilities
│   │   │   └── exceptions.py        # Custom exceptions
│   │   ├── models/                  # Database models
│   │   │   └── __init__.py
│   │   ├── schemas/                 # Pydantic schemas
│   │   │   └── __init__.py
│   │   ├── services/                # Business logic
│   │   │   └── __init__.py
│   │   ├── utils/                   # Utility functions
│   │   │   ├── __init__.py
│   │   │   └── helpers.py
│   │   └── middleware/              # Custom middleware
│   │       └── __init__.py
│   └── main.py                      # Application entry point
│
├── 🧪 Testing
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py              # Pytest configuration
│   │   ├── test_main.py             # Main app tests
│   │   ├── api/                     # API tests
│   │   │   ├── __init__.py
│   │   │   └── test_v1/
│   │   │       └── __init__.py
│   │   └── utils/                   # Utility tests
│   │       └── __init__.py
│
├── 📚 Documentation
│   ├── docs/
│   │   ├── README.md
│   │   ├── api.md                   # API documentation
│   │   └── deployment.md            # Deployment guide
│
├── 🔧 Configuration
│   ├── .env.example                 # Environment variables template
│   ├── .gitignore                   # Git ignore rules
│   ├── pyproject.toml               # Project configuration (Poetry)
│   ├── requirements.txt             # Dependencies (pip)
│   ├── pytest.ini                  # Pytest configuration
│   └── .pre-commit-config.yaml      # Pre-commit hooks
│
└── 📋 Project Files
    ├── README.md                    # Project documentation
    ├── CHANGELOG.md                 # Version history
    └── LICENSE                      # License file
```

## 🔐 With Authentication: `fastkit add auth jwt`

After adding JWT authentication, the structure expands:

```
my-project/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py
│   │       └── endpoints/           # 🆕 API endpoints
│   │           ├── __init__.py
│   │           ├── auth.py          # 🆕 Authentication endpoints
│   │           └── users.py         # 🆕 User management endpoints
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py              # 🔄 Enhanced with JWT utilities
│   │   └── auth/                    # 🆕 Authentication module
│   │       ├── __init__.py
│   │       ├── jwt.py               # 🆕 JWT token handling
│   │       ├── password.py          # 🆕 Password hashing
│   │       └── permissions.py       # 🆕 Permission system
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py                  # 🆕 User model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                  # 🆕 Auth schemas
│   │   └── user.py                  # 🆕 User schemas
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py          # 🆕 Authentication service
│       └── user_service.py          # 🆕 User management service
│
├── tests/
│   ├── api/
│   │   └── test_v1/
│   │       ├── test_auth.py         # 🆕 Auth endpoint tests
│   │       └── test_users.py        # 🆕 User endpoint tests
│   └── services/
│       ├── test_auth_service.py     # 🆕 Auth service tests
│       └── test_user_service.py     # 🆕 User service tests
│
└── .env.example                     # 🔄 Updated with JWT settings
```

## 🗄️ With Database: `fastkit add database postgresql`

After adding PostgreSQL database support:

```
my-project/
├── app/
│   ├── core/
│   │   ├── config.py                # 🔄 Updated with DB settings
│   │   └── database/                # 🆕 Database configuration
│   │       ├── __init__.py
│   │       ├── connection.py        # 🆕 Database connection
│   │       ├── session.py           # 🆕 Database session
│   │       └── base.py              # 🆕 Base model class
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                  # 🆕 Base model
│   │   └── user.py                  # 🔄 Enhanced with SQLAlchemy
│   └── services/
│       ├── __init__.py
│       └── database_service.py      # 🆕 Database utilities
│
├── 🗄️ Database
│   ├── alembic/                     # 🆕 Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── alembic.ini
│   └── migrations/                  # 🆕 Migration scripts
│       └── __init__.py
│
├── scripts/                         # 🆕 Database scripts
│   ├── init_db.py                   # 🆕 Database initialization
│   └── reset_db.py                  # 🆕 Database reset
│
└── .env.example                     # 🔄 Updated with DB credentials
```

## ⚡ With Cache: `fastkit add cache redis`

After adding Redis caching:

```
my-project/
├── app/
│   ├── core/
│   │   ├── config.py                # 🔄 Updated with Redis settings
│   │   └── cache/                   # 🆕 Cache configuration
│   │       ├── __init__.py
│   │       ├── redis.py             # 🆕 Redis connection
│   │       └── decorators.py        # 🆕 Caching decorators
│   ├── services/
│   │   ├── __init__.py
│   │   └── cache_service.py         # 🆕 Cache service
│   └── utils/
│       ├── __init__.py
│       └── cache_keys.py            # 🆕 Cache key utilities
│
└── .env.example                     # 🔄 Updated with Redis settings
```

## 🏗️ With Domain: `fastkit create-domain users`

After creating a "users" domain:

```
my-project/
├── app/
│   ├── domains/                     # 🆕 Domain-driven structure
│   │   ├── __init__.py
│   │   └── users/                   # 🆕 Users domain
│   │       ├── __init__.py
│   │       ├── models/              # 🆕 User domain models
│   │       │   ├── __init__.py
│   │       │   └── user.py
│   │       ├── schemas/             # 🆕 User domain schemas
│   │       │   ├── __init__.py
│   │       │   ├── user.py
│   │       │   └── user_create.py
│   │       ├── services/            # 🆕 User domain services
│   │       │   ├── __init__.py
│   │       │   ├── user_service.py
│   │       │   └── user_repository.py
│   │       ├── api/                 # 🆕 User domain API
│   │       │   ├── __init__.py
│   │       │   └── users.py
│   │       └── exceptions/          # 🆕 User domain exceptions
│   │           ├── __init__.py
│   │           └── user_exceptions.py
│   │
│   └── api/
│       └── v1/
│           ├── api.py               # 🔄 Updated to include user routes
│           └── endpoints/
│               └── users.py         # 🔄 Enhanced user endpoints
│
├── tests/
│   └── domains/                     # 🆕 Domain tests
│       └── users/
│           ├── __init__.py
│           ├── test_user_service.py
│           ├── test_user_repository.py
│           └── api/
│               └── test_users.py
│
└── docs/
    └── domains/                     # 🆕 Domain documentation
        └── users.md
```

## 🐳 With Deployment: `fastkit deploy docker`

After adding Docker deployment:

```
my-project/
├── 🐳 Docker Configuration
│   ├── Dockerfile                   # 🆕 Main Dockerfile
│   ├── docker-compose.yml           # 🆕 Docker Compose
│   ├── docker-compose.dev.yml       # 🆕 Development compose
│   ├── docker-compose.prod.yml      # 🆕 Production compose
│   ├── .dockerignore                # 🆕 Docker ignore rules
│   └── docker/                      # 🆕 Docker configurations
│       ├── nginx/
│       │   └── nginx.conf           # 🆕 Nginx configuration
│       ├── postgres/
│       │   └── init.sql             # 🆕 Database initialization
│       └── redis/
│           └── redis.conf           # 🆕 Redis configuration
│
├── 📜 Scripts
│   ├── scripts/
│   │   ├── docker-build.sh          # 🆕 Docker build script
│   │   ├── docker-run.sh            # 🆕 Docker run script
│   │   └── deploy.sh                # 🆕 Deployment script
│
└── 🔧 Environment Files
    ├── .env.docker                  # 🆕 Docker environment
    ├── .env.production              # 🆕 Production environment
    └── .env.staging                 # 🆕 Staging environment
```

## 🚀 Complete Project Structure

Here's what a fully-featured project looks like after using all FastKit features:

```
my-project/
├── 📱 Application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── api.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── auth.py
│   │   │           ├── users.py
│   │   │           └── health.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── exceptions.py
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── jwt.py
│   │   │   │   ├── password.py
│   │   │   │   └── permissions.py
│   │   │   ├── database/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── connection.py
│   │   │   │   ├── session.py
│   │   │   │   └── base.py
│   │   │   └── cache/
│   │   │       ├── __init__.py
│   │   │       ├── redis.py
│   │   │       └── decorators.py
│   │   ├── domains/
│   │   │   ├── __init__.py
│   │   │   └── users/
│   │   │       ├── __init__.py
│   │   │       ├── models/
│   │   │       ├── schemas/
│   │   │       ├── services/
│   │   │       ├── api/
│   │   │       └── exceptions/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── cache_service.py
│   │   │   └── database_service.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── helpers.py
│   │   │   └── cache_keys.py
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── cors.py
│   │       ├── logging.py
│   │       └── rate_limiting.py
│   └── main.py
│
├── 🗄️ Database
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── alembic.ini
│   ├── migrations/
│   │   └── __init__.py
│   └── scripts/
│       ├── init_db.py
│       └── reset_db.py
│
├── 🧪 Testing
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── test_v1/
│   │   │       ├── __init__.py
│   │   │       ├── test_auth.py
│   │   │       └── test_users.py
│   │   ├── domains/
│   │   │   └── users/
│   │   │       ├── __init__.py
│   │   │       ├── test_user_service.py
│   │   │       └── api/
│   │   │           └── test_users.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── test_auth_service.py
│   │   │   └── test_user_service.py
│   │   └── utils/
│   │       └── __init__.py
│
├── 🐳 Deployment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   ├── .dockerignore
│   ├── docker/
│   │   ├── nginx/
│   │   │   └── nginx.conf
│   │   ├── postgres/
│   │   │   └── init.sql
│   │   └── redis/
│   │       └── redis.conf
│   └── scripts/
│       ├── docker-build.sh
│       ├── docker-run.sh
│       └── deploy.sh
│
├── 📚 Documentation
│   ├── docs/
│   │   ├── README.md
│   │   ├── api.md
│   │   ├── deployment.md
│   │   ├── development.md
│   │   └── domains/
│   │       └── users.md
│
├── 🔧 Configuration
│   ├── .env.example
│   ├── .env.docker
│   ├── .env.production
│   ├── .env.staging
│   ├── .gitignore
│   ├── .editorconfig
│   ├── .pre-commit-config.yaml
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── ruff.toml
│   └── mypy.ini
│
└── 📋 Project Files
    ├── README.md
    ├── CHANGELOG.md
    ├── LICENSE
    └── Makefile
```

## 🎯 Key Features of Generated Projects

### **1. Scalable Architecture**
- **Domain-driven design** for complex applications
- **Layered architecture** with clear separation of concerns
- **Modular structure** that grows with your project

### **2. Best Practices Built-in**
- **Type hints** throughout the codebase
- **Pydantic schemas** for data validation
- **Dependency injection** with FastAPI
- **Error handling** and custom exceptions

### **3. Development Ready**
- **Testing infrastructure** with pytest
- **Code quality tools** (ruff, mypy, pre-commit)
- **Development scripts** and utilities
- **Hot reload** and debugging support

### **4. Production Ready**
- **Docker containerization**
- **Database migrations** with Alembic
- **Caching strategies** with Redis
- **Security** with JWT authentication
- **Monitoring** and logging setup

### **5. Documentation**
- **API documentation** with FastAPI's automatic docs
- **Project documentation** with guides and examples
- **Code documentation** with docstrings
- **Deployment guides** for different platforms

This structure ensures that users get a **professional, scalable, and maintainable** FastAPI project right from the start! 🚀