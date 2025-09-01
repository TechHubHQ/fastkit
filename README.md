# FastKit

🚀 A powerful FastAPI project generator and toolkit

FastKit is a CLI tool that helps you scaffold FastAPI projects with best practices, integrations, and deployment configurations.

## Features

- Interactive project creation with step-by-step setup
- Authentication options (JWT, OAuth, Session-based)
- Database integrations (SQLite, PostgreSQL)
- Caching solutions (Redis, Memcached)
- Domain-driven architecture support
- Deployment configurations (Docker, Kubernetes, Heroku)
- Extensible plugin system

## Installation

```bash
pip install fastkit
```

## Quick Start

```bash
# Create a new FastAPI project
fastkit new my-project

# Add a new domain to existing project
fastkit create-domain user

# Add integrations
fastkit add auth jwt
fastkit add database postgresql
fastkit add cache redis

# Generate deployment configs
fastkit deploy docker
```

## Documentation

See the [docs](./docs/) directory for detailed documentation.