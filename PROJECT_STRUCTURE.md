# FastKit Project Structure

This document provides a comprehensive overview of the FastKit project structure.

## 📁 Root Directory Structure

```
fastkit/
├── 🚀 CLI Layer
│   ├── cli/                          # Command-line interface
│   │   ├── __init__.py
│   │   ├── main.py                   # Main CLI entry point
│   │   ├── commands/                 # CLI commands
│   │   │   ├── __init__.py
│   │   │   ├── new.py               # fastkit new <project-name>
│   │   │   ├── create_domain.py     # fastkit create-domain <domain-name>
│   │   │   ├── add.py               # fastkit add <integration>
│   │   │   ├── deploy.py            # fastkit deploy <platform>
│   │   │   ├── info.py              # fastkit info
│   │   │   ├── generate.py          # fastkit generate <component>
│   │   │   ├── init.py              # fastkit init
│   │   │   ├── serve.py             # fastkit serve
│   │   │   └── migrate.py           # fastkit migrate
│   │   ├── prompts/                 # Interactive prompts
│   │   │   ├── __init__.py
│   │   │   ├── project_setup.py     # Project setup wizard
│   │   │   ├── auth_setup.py        # Auth configuration prompts
│   │   │   ├── database_setup.py    # Database setup prompts
│   │   │   ├── cache_setup.py       # Cache setup prompts
│   │   │   └── deployment_setup.py  # Deployment prompts
│   │   └── validators/              # Input validation
│   │       ├── __init__.py
│   │       ├── project.py           # Project name validators
│   │       └── domain.py            # Domain name validators
│
├── ⚙️ Generators Layer
│   ├── generators/                   # Code generation logic
│   │   ├── __init__.py
│   │   ├── project/                 # Project scaffolding
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # Base project generator
│   │   │   └── structure.py         # Directory structure generator
│   │   ├── auth/                    # Authentication generators
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py               # JWT authentication
│   │   │   ├── oauth.py             # OAuth authentication
│   │   │   └── session.py           # Session-based auth
│   │   ├── database/                # Database integrations
│   │   │   ├── __init__.py
│   │   │   ├── sqlite.py            # SQLite generator
│   │   │   ├── postgresql.py        # PostgreSQL generator
│   │   │   └── models.py            # Database models generator
│   │   ├── cache/                   # Caching solutions
│   │   │   ├── __init__.py
│   │   │   ├── redis.py             # Redis cache generator
│   │   │   └── memcached.py         # Memcached generator
│   │   ├── domain/                  # Domain creation
│   │   │   ├── __init__.py
│   │   │   ├── crud.py              # CRUD operations generator
│   │   │   ├── api.py               # API endpoints generator
│   │   │   ├── models.py            # Domain models generator
│   │   │   └── schemas.py           # Pydantic schemas generator
│   │   ├── middleware/              # Middleware generators
│   │   │   ├── __init__.py
│   │   │   ├── cors.py              # CORS middleware
│   │   │   ├── logging.py           # Logging middleware
│   │   │   └── rate_limiting.py     # Rate limiting middleware
│   │   ├── services/                # Service generators
│   │   │   ├── __init__.py
│   │   │   ├── email.py             # Email service
│   │   │   ├── file_storage.py      # File storage service
│   │   │   └── notification.py      # Notification service
│   │   └── deployment/              # Deployment configurations
│   │       ├── __init__.py
│   │       ├── docker.py            # Docker generator
│   │       ├── kubernetes.py        # Kubernetes generator
│   │       └── heroku.py            # Heroku generator
│
├── 📄 Templates Layer
│   ├── templates/                   # Jinja2 templates
│   │   ├── __init__.py
│   │   ├── project/                 # Base project templates
│   │   │   ├── main.py.j2           # FastAPI main app template
│   │   │   ├── pyproject.toml.j2    # Project config template
│   │   │   ├── requirements.txt.j2   # Requirements template
│   │   │   ├── README.md.j2         # Project README template
│   │   │   ├── .env.example.j2      # Environment variables template
│   │   │   ├── .gitignore.j2        # Gitignore template
│   │   │   ├── app/                 # App structure templates
│   │   │   │   ├── __init__.py.j2
│   │   │   │   ├── api/__init__.py.j2
│   │   │   │   └── core/
│   │   │   │       ├── __init__.py.j2
│   │   │   │       └── config.py.j2
│   │   │   ├── tests/               # Test templates
│   │   │   └── docs/                # Documentation templates
│   │   ├── auth/                    # Authentication templates
│   │   │   ├── jwt_auth.py.j2       # JWT auth template
│   │   │   └── oauth_auth.py.j2     # OAuth auth template
│   │   ├── database/                # Database templates
│   │   │   ├── sqlite_config.py.j2  # SQLite config template
│   │   │   └── postgresql_config.py.j2 # PostgreSQL config template
│   │   ├── cache/                   # Cache templates
│   │   │   └── redis_config.py.j2   # Redis config template
│   │   ├── domain/                  # Domain templates
│   │   │   ├── router.py.j2         # Domain router template
│   │   │   ├── model.py.j2          # Domain model template
│   │   │   └── schema.py.j2         # Domain schema template
│   │   ├── middleware/              # Middleware templates
│   │   │   ├── cors.py.j2           # CORS middleware template
│   │   │   └── logging.py.j2        # Logging middleware template
│   │   ├── services/                # Service templates
│   │   │   ├── email.py.j2          # Email service template
│   │   │   └── file_storage.py.j2   # File storage service template
│   │   └── deployment/              # Deployment templates
│   │       ├── Dockerfile.j2        # Dockerfile template
│   │       ├── docker-compose.yml.j2 # Docker Compose template
│   │       ├── kubernetes.yaml.j2   # Kubernetes template
│   │       ├── .dockerignore.j2     # Dockerignore template
│   │       ├── nginx.conf.j2        # Nginx config template
│   │       ├── Procfile.j2          # Heroku Procfile template
│   │       └── railway.toml.j2      # Railway deployment template
│
├── 🔧 Core Layer
│   ├── core/                        # Core functionality
│   │   ├── __init__.py
│   │   ├── config/                  # Configuration management
│   │   │   ├── __init__.py
│   │   │   ├── settings.py          # FastKit settings
│   │   │   └── project_config.py    # Project-specific config
│   │   ├── project/                 # Project management
│   │   │   ├── __init__.py
│   │   │   ├── detector.py          # FastKit project detection
│   │   │   └── manager.py           # Project management utilities
│   │   └── plugins/                 # Plugin system
│   │       ├── __init__.py
│   │       ├── base.py              # Base plugin interface
│   │       └── loader.py            # Plugin loader
│
├── 🛠️ Utilities & Support
│   ├── utils/                       # Utility functions
│   │   ├── __init__.py
│   │   ├── file_operations.py       # File/directory operations
│   │   ├── template_engine.py       # Jinja2 template engine
│   │   ├── console.py               # Console output utilities
│   │   ├── validators.py            # Common validators
│   │   ├── git.py                   # Git operations utilities
│   │   ├── dependencies.py          # Dependency management
│   │   ├── spinner.py               # Loading spinner utilities
│   │   └── network.py               # Network utilities
│   ├── schemas/                     # Configuration schemas
│   │   ├── __init__.py
│   │   ├── project.py               # Project configuration schemas
│   │   ├── integration.py           # Integration configuration schemas
│   │   └── domain.py                # Domain configuration schemas
│   ├── exceptions/                  # Custom exceptions
│   │   ├── __init__.py
│   │   ├── cli.py                   # CLI exceptions
│   │   ├── generator.py             # Generator exceptions
│   │   └── project.py               # Project exceptions
│   ├── integrations/                # Service integrations
│   │   ├── __init__.py
│   │   ├── monitoring/              # Monitoring integrations
│   │   │   ├── __init__.py
│   │   │   ├── prometheus.py        # Prometheus integration
│   │   │   └── sentry.py            # Sentry integration
│   │   ├── testing/                 # Testing integrations
│   │   │   ├── __init__.py
│   │   │   ├── pytest.py            # Pytest integration
│   │   │   └── coverage.py          # Coverage integration
│   │   └── logging/                 # Logging integrations
│   │       ├── __init__.py
│   │       ├── structured.py        # Structured logging
│   │       └── elk.py               # ELK Stack integration
│   ├── config/                      # Configuration files
│   │   └── default.yaml             # Default configuration
│   ├── __init__.py                  # Main package init
│   ├── __main__.py                  # Entry point for python -m fastkit
│   ├── py.typed                     # PEP 561 marker file
│   ├── constants.py                 # FastKit constants
│   └── version.py                   # Version information
│
├── 🧪 Testing
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py              # Pytest configuration
│   │   ├── fixtures/                # Test fixtures
│   │   │   ├── __init__.py
│   │   │   ├── project_configs.py   # Project config fixtures
│   │   │   └── templates.py         # Template fixtures
│   │   ├── unit/                    # Unit tests
│   │   │   ├── __init__.py
│   │   │   ├── test_cli.py          # CLI unit tests
│   │   │   ├── test_generators.py   # Generator tests
│   │   │   ├── test_utils.py        # Utility tests
│   │   │   ├── test_core.py         # Core functionality tests
│   │   │   └── test_templates.py    # Template rendering tests
│   │   └── integration/             # Integration tests
│   │       ├── __init__.py
│   │       ├── test_project_generation.py # Project generation tests
│   │       ├── test_domain_creation.py    # Domain creation tests
│   │       └── test_cli_commands.py       # CLI commands tests
│
├── 📚 Documentation & Examples
│   ├── docs/
│   │   ├── README.md                # Documentation overview
│   │   ├── getting-started.md       # Getting started guide
│   │   ├── commands.md              # CLI commands reference
│   │   ├── integrations.md          # Available integrations
│   │   ├── architecture.md          # Architecture documentation
│   │   ├── development.md           # Development guide
│   │   ├── plugins.md               # Plugin development guide
│   │   ├── templates.md             # Template customization guide
│   │   └── troubleshooting.md       # Troubleshooting guide
│   ├── examples/
│   │   ├── basic_project.py         # Basic project example
│   │   ├── with_auth.py             # Project with auth example
│   │   ├── full_stack.py            # Full-stack example
│   │   ├── microservices.py         # Microservices example
│   │   ├── api_gateway.py           # API Gateway example
│   │   └── custom_plugin.py         # Custom plugin example
│
├── 🔄 CI/CD & Configuration
│   ├── .github/
│   │   └── workflows/
│   │       └── ci.yml               # GitHub Actions CI
│   ├── .editorconfig                # Editor configuration
│   ├── .pre-commit-config.yaml      # Pre-commit hooks
│   ├── ruff.toml                    # Ruff linting config
│   ├── mypy.ini                     # MyPy type checking config
│   ├── pytest.ini                  # Pytest configuration
│   └── Makefile                     # Development commands
│
└── 📋 Project Files
    ├── README.md                    # Main project README
    ├── PROJECT_STRUCTURE.md         # This file
    ├── CHANGELOG.md                 # Version changelog
    ├── CONTRIBUTING.md              # Contribution guidelines
    ├── LICENSE                      # License file
    ├── pyproject.toml               # Project configuration
    ├── poetry.lock                  # Dependency lock file
    └── .gitignore                   # Git ignore rules
```

## 🎯 Key Components

### CLI Commands
- `fastkit new <project-name>` - Create new FastAPI project
- `fastkit create-domain <domain-name>` - Add domain to existing project
- `fastkit add <integration>` - Add auth, database, cache integrations
- `fastkit deploy <platform>` - Generate deployment configurations
- `fastkit generate <component>` - Generate specific components
- `fastkit init` - Initialize FastKit in existing directory
- `fastkit serve` - Start development server
- `fastkit migrate` - Run database migrations
- `fastkit info` - Show project information

### Supported Integrations
- **Authentication**: JWT, OAuth, Session-based
- **Databases**: SQLite, PostgreSQL
- **Caching**: Redis, Memcached
- **Monitoring**: Prometheus, Sentry
- **Testing**: Pytest, Coverage
- **Logging**: Structured logging, ELK Stack
- **Deployment**: Docker, Kubernetes, Heroku, Railway

### Architecture Principles
- **Modular Design**: Clear separation of concerns
- **Template-driven**: Jinja2 templates for code generation
- **Plugin System**: Extensible architecture
- **Type Safety**: Full type hints and MyPy support
- **Testing**: Comprehensive test coverage
- **Documentation**: Complete documentation and examples

This structure provides a solid foundation for building a production-ready CLI toolkit for FastAPI development.