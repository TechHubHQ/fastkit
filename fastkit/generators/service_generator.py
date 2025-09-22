"""Service generator for adding services to existing projects."""

import re
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader

from .utils import ensure_dir, render_and_write
from .dependency_manager import get_dependency_manager
from .db_generator import generate_database_setup, update_database_configuration, ensure_database_imports_in_main
from .cache_generator import generate_cache_setup, update_cache_configuration, ensure_cache_imports_in_main
from .auth_generator import generate_auth_setup, update_auth_configuration, ensure_auth_imports_in_main, generate_auth_dependencies


def add_service_to_project(
    project_path: Path,
    service_type: str,
    service_provider: str,
    force: bool = False
) -> None:
    """Add a service to an existing FastKit project."""

    # Read current project configuration
    project_config = _read_project_config(project_path)

    # Update configuration with new service
    if service_type == "db":
        project_config["db_choice"] = service_provider
    elif service_type == "cache":
        project_config["cache_choice"] = service_provider
    elif service_type == "auth":
        project_config["auth_type"] = service_provider
    elif service_type == "jobs":
        project_config["jobs_choice"] = service_provider

    # Create service files
    _create_service_files(project_path, service_type,
                          service_provider, project_config)

    # Update configuration files
    _update_config_files(project_path, project_config)

    # Sync dependencies using dependency manager
    dep_manager = get_dependency_manager(project_path)
    dep_manager.sync_service_dependencies(service_type, service_provider)


def _read_project_config(project_path: Path) -> Dict[str, Any]:
    """Read current project configuration from pyproject.toml."""
    pyproject_path = project_path / "pyproject.toml"

    if not pyproject_path.exists():
        raise FileNotFoundError(
            "pyproject.toml not found. Is this a FastKit project?")

    # Basic configuration extraction - in a real implementation, you might want to use toml library
    content = pyproject_path.read_text(encoding='utf-8')

    # Extract project name
    project_name_match = re.search(r'name = "([^"]+)"', content)
    project_name = project_name_match.group(
        1) if project_name_match else "unknown"

    # Determine current services by checking dependencies
    config = {
        "project_name": project_name,
        "db_choice": "none",
        "cache_choice": "none",
        "auth_type": "none",
        "architecture": "rest-apis",  # Default assumption
        "include_cicd": True,
        "include_docker": True
    }

    # Check existing dependencies to determine current services
    if "redis" in content:
        config["cache_choice"] = "redis"
    elif "pymemcache" in content:
        config["cache_choice"] = "memcached"
    elif "boto3" in content:
        config["cache_choice"] = "dynamodb"
    elif "cachetools" in content:
        config["cache_choice"] = "in-memory"

    if "psycopg2" in content:
        config["db_choice"] = "postgresql"
    elif "pymysql" in content:
        config["db_choice"] = "mysql"
    elif "sqlalchemy" in content and "sqlite" not in content:
        config["db_choice"] = "sqlite"

    if "python-jose" in content or "PyJWT" in content:
        config["auth_type"] = "jwt"
    elif "authlib" in content:
        config["auth_type"] = "oauth"

    return config


def _create_service_files(
    project_path: Path,
    service_type: str,
    service_provider: str,
    config: Dict[str, Any]
) -> None:
    """Create service-specific files."""

    # Initialize Jinja2 environment
    templates_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(templates_dir),
                      trim_blocks=False, lstrip_blocks=False)

    # Update config with new service
    if service_type == "db":
        config["db_choice"] = service_provider
    elif service_type == "cache":
        config["cache_choice"] = service_provider
    elif service_type == "auth":
        config["auth_type"] = service_provider
    elif service_type == "jobs":
        config["jobs_choice"] = service_provider

    # Create service directory (except for db, cache, auth which are handled by unified generators)
    if service_type not in ["db", "cache", "auth"]:
        service_dir = project_path / "app" / service_type
        ensure_dir(service_dir)
    else:
        service_dir = project_path / "app" / service_type  # For reference in other service types

    # Render service templates
    if service_type == "cache":
        # Use the unified cache generator to ensure consistency with project creation
        generate_cache_setup(
            project_path,
            service_provider,
            config["project_name"],
            template_env=env
        )
        
        # Update configuration files
        update_cache_configuration(project_path, service_provider, config["project_name"])
        
        # Ensure proper imports in main.py
        ensure_cache_imports_in_main(project_path, service_provider)

    elif service_type == "db":
        # Use the unified database generator to ensure consistency with project creation
        generate_database_setup(
            project_path,
            service_provider,
            config["project_name"],
            template_env=env
        )
        
        # Update configuration files
        update_database_configuration(project_path, service_provider, config["project_name"])
        
        # Ensure proper imports in main.py
        ensure_database_imports_in_main(project_path, service_provider)

    elif service_type == "auth":
        # Use the unified auth generator to ensure consistency with project creation
        generate_auth_setup(
            project_path,
            service_provider,
            config["project_name"],
            template_env=env
        )
        
        # Update configuration files
        update_auth_configuration(project_path, service_provider, config["project_name"])
        
        # Ensure proper imports in main.py
        ensure_auth_imports_in_main(project_path, service_provider)
        
        # Generate auth dependencies for FastAPI
        generate_auth_dependencies(project_path, service_provider)

    elif service_type == "jobs":
        _render_and_write_with_env(
            env, f"services/jobs/__init__.py.jinja",
            service_dir / "__init__.py", config
        )
        
        # Create specific job scheduler based on provider
        if service_provider == "celery":
            _render_and_write_with_env(
                env, f"services/jobs/celery_scheduler.py.jinja",
                service_dir / "celery_scheduler.py", config
            )
        elif service_provider == "rq":
            _render_and_write_with_env(
                env, f"services/jobs/rq_scheduler.py.jinja",
                service_dir / "rq_scheduler.py", config
            )
        elif service_provider == "apscheduler":
            _render_and_write_with_env(
                env, f"services/jobs/apscheduler_scheduler.py.jinja",
                service_dir / "apscheduler_scheduler.py", config
            )
        elif service_provider == "dramatiq":
            _render_and_write_with_env(
                env, f"services/jobs/dramatiq_scheduler.py.jinja",
                service_dir / "dramatiq_scheduler.py", config
            )
        elif service_provider == "arq":
            _render_and_write_with_env(
                env, f"services/jobs/arq_scheduler.py.jinja",
                service_dir / "arq_scheduler.py", config
            )
        
        # Create example tasks file
        _render_and_write_with_env(
            env, f"services/jobs/tasks.py.jinja",
            service_dir / "tasks.py", config
        )


def _render_and_write_with_env(env: Environment, template_name: str, dest_path: Path, context: dict) -> None:
    """Render template with given environment and write to destination."""
    render_and_write(template_name, dest_path, context, env)


def _update_config_files(project_path: Path, config: Dict[str, Any]) -> None:
    """Update configuration files with new service settings."""

    # Update app/core/config.py
    config_path = project_path / "app" / "core" / "config.py"
    if config_path.exists():
        _update_app_config(config_path, config)


def _update_app_config(config_path: Path, config: Dict[str, Any]) -> None:
    """Update app/core/config.py with new service configurations."""

    content = config_path.read_text(encoding='utf-8')

    # Add database settings if not present
    if config["db_choice"] != "none" and "# Database settings" not in content:
        db_config = _generate_db_config(config)
        # Insert before the last class Config section
        content = content.replace(
            "    class Config:",
            f"{db_config}\n    class Config:"
        )

    # Add cache settings if not present
    if config["cache_choice"] != "none" and "# Cache settings" not in content:
        cache_config = _generate_cache_config(config)
        # Insert before the last class Config section
        content = content.replace(
            "    class Config:",
            f"{cache_config}\n    class Config:"
        )

    config_path.write_text(content, encoding='utf-8')


def _generate_db_config(config: Dict[str, Any]) -> str:
    """Generate database configuration section."""
    db_choice = config["db_choice"]
    project_name = config["project_name"]

    db_configs = {
        "postgresql": f'    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/{project_name.replace("-", "_")}_db")',
        "mysql": f'    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql://user:password@localhost/{project_name.replace("-", "_")}_db")',
        "sqlite": f'    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./{project_name.replace("-", "_")}.db")',
        "mongodb": f'    DATABASE_URL: str = os.getenv("DATABASE_URL", "mongodb://localhost:27017/{project_name.replace("-", "_")}_db")',
        "mssql": f'    DATABASE_URL: str = os.getenv("DATABASE_URL", "mssql://user:password@localhost/{project_name.replace("-", "_")}_db")'
    }

    return f"""
    # Database settings
{db_configs.get(db_choice, "")}"""


def _generate_cache_config(config: Dict[str, Any]) -> str:
    """Generate cache configuration section."""
    cache_choice = config["cache_choice"]
    project_name = config["project_name"]

    cache_configs = {
        "redis": '''    # Cache settings
    CACHE_TTL: int = 300  # 5 minutes default TTL
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")''',
        "memcached": '''    # Cache settings
    CACHE_TTL: int = 300  # 5 minutes default TTL
    MEMCACHED_SERVERS: str = os.getenv("MEMCACHED_SERVERS", "localhost:11211")''',
        "dynamodb": f'''    # Cache settings
    CACHE_TTL: int = 300  # 5 minutes default TTL
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_TABLE_NAME: str = os.getenv("DYNAMODB_TABLE_NAME", "{project_name.replace("-", "_")}_cache")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")''',
        "in-memory": '''    # Cache settings
    CACHE_TTL: int = 300  # 5 minutes default TTL
    CACHE_MAX_SIZE: int = 1000  # Maximum number of items in cache'''
    }

    return cache_configs.get(cache_choice, "")
