"""Cleanup utilities for removing previous service configurations."""

import re
from pathlib import Path
from typing import List, Set


def cleanup_cache_files(project_path: Path) -> None:
    """Remove all existing cache-related files."""
    cache_dir = project_path / "app" / "cache"

    if not cache_dir.exists():
        return

    # List of cache client files to remove
    cache_files = [
        "redis_client.py",
        "memcached_client.py",
        "memory_client.py",
    ]

    for cache_file in cache_files:
        file_path = cache_dir / cache_file
        if file_path.exists():
            file_path.unlink()


def cleanup_cache_config(project_path: Path) -> None:
    """Remove cache configuration from config.py."""
    config_path = project_path / "app" / "core" / "config.py"

    if not config_path.exists():
        return

    content = config_path.read_text(encoding='utf-8')

    # Remove cache settings section
    # Pattern to match cache settings block
    cache_patterns = [
        r'    # Cache settings\n.*?(?=\n    [A-Z]|\n    class|\nclass|\Z)',
        r'    CACHE_TTL:.*?\n',
        r'    REDIS_URL:.*?\n',
        r'    MEMCACHED_SERVERS:.*?\n',
        r'    CACHE_MAX_SIZE:.*?\n'
    ]

    for pattern in cache_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Clean up extra newlines
    content = re.sub(r'\n\n\n+', '\n\n', content)

    config_path.write_text(content, encoding='utf-8')


def cleanup_cache_imports(project_path: Path) -> None:
    """Remove cache imports from main.py."""
    main_path = project_path / "app" / "main.py"

    if not main_path.exists():
        return

    content = main_path.read_text(encoding='utf-8')

    # Remove cache import lines
    cache_import_patterns = [
        r'from app\.cache import.*?\n',
        r'import app\.cache.*?\n'
    ]

    for pattern in cache_import_patterns:
        content = re.sub(pattern, '', content)

    main_path.write_text(content, encoding='utf-8')


def cleanup_database_files(project_path: Path) -> None:
    """Remove all existing database-related files."""
    db_dir = project_path / "app" / "db"

    if not db_dir.exists():
        return

    # List of database files to remove (keep __init__.py and session.py as they're generic)
    db_files = [
        "base.py",
        "base_model.py",
        "postgresql_client.py",
        "mysql_client.py",
        "sqlite_client.py",
        "mongodb_client.py",
        "mssql_client.py"
    ]

    for db_file in db_files:
        file_path = db_dir / db_file
        if file_path.exists():
            file_path.unlink()


def cleanup_database_config(project_path: Path) -> None:
    """Remove database configuration from config.py."""
    config_path = project_path / "app" / "core" / "config.py"

    if not config_path.exists():
        return

    content = config_path.read_text(encoding='utf-8')

    # Remove database settings section
    db_patterns = [
        r'    # Database settings\n.*?(?=\n    [A-Z]|\n    class|\nclass|\Z)',
        r'    DATABASE_URL:.*?\n'
    ]

    for pattern in db_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Clean up extra newlines
    content = re.sub(r'\n\n\n+', '\n\n', content)

    config_path.write_text(content, encoding='utf-8')


def cleanup_database_imports(project_path: Path) -> None:
    """Remove database imports from main.py."""
    main_path = project_path / "app" / "main.py"

    if not main_path.exists():
        return

    content = main_path.read_text(encoding='utf-8')

    # Remove database import lines
    db_import_patterns = [
        r'from app\.db import.*?\n',
        r'import app\.db.*?\n'
    ]

    for pattern in db_import_patterns:
        content = re.sub(pattern, '', content)

    main_path.write_text(content, encoding='utf-8')


def cleanup_auth_files(project_path: Path) -> None:
    """Remove all existing auth-related files."""
    auth_dir = project_path / "app" / "auth"

    if not auth_dir.exists():
        return

    # List of auth files to remove
    auth_files = [
        "jwt_provider.py",
        "oauth_provider.py",
        "auth_service.py",
        "models.py",
        "schemas.py"
    ]

    for auth_file in auth_files:
        file_path = auth_dir / auth_file
        if file_path.exists():
            file_path.unlink()


def cleanup_auth_config(project_path: Path) -> None:
    """Remove auth configuration from config.py."""
    config_path = project_path / "app" / "core" / "config.py"

    if not config_path.exists():
        return

    content = config_path.read_text(encoding='utf-8')

    # Remove auth settings section
    auth_patterns = [
        r'    # Authentication settings\n.*?(?=\n    [A-Z]|\n    class|\nclass|\Z)',
        r'    SECRET_KEY:.*?\n',
        r'    ACCESS_TOKEN_EXPIRE_MINUTES:.*?\n',
        r'    REFRESH_TOKEN_EXPIRE_DAYS:.*?\n',
        r'    OAUTH_CLIENT_ID:.*?\n',
        r'    OAUTH_CLIENT_SECRET:.*?\n',
        r'    OAUTH_REDIRECT_URI:.*?\n',
        r'    OAUTH_PROVIDER_URL:.*?\n'
    ]

    for pattern in auth_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Clean up extra newlines
    content = re.sub(r'\n\n\n+', '\n\n', content)

    config_path.write_text(content, encoding='utf-8')


def cleanup_auth_imports(project_path: Path) -> None:
    """Remove auth imports from main.py."""
    main_path = project_path / "app" / "main.py"

    if not main_path.exists():
        return

    content = main_path.read_text(encoding='utf-8')

    # Remove auth import lines
    auth_import_patterns = [
        r'from app\.auth import.*?\n',
        r'import app\.auth.*?\n'
    ]

    for pattern in auth_import_patterns:
        content = re.sub(pattern, '', content)

    main_path.write_text(content, encoding='utf-8')


def cleanup_auth_dependencies(project_path: Path) -> None:
    """Remove auth dependencies from dependencies.py."""
    dependencies_path = project_path / "app" / "core" / "dependencies.py"

    if not dependencies_path.exists():
        return

    content = dependencies_path.read_text(encoding='utf-8')

    # Remove auth dependencies section
    auth_dep_patterns = [
        r'# Authentication dependencies\n.*?(?=\n# |\nclass |\ndef |\Z)',
        r'from app\.auth import.*?\n',
        r'security = HTTPBearer\(\)\n',
        r'def get_current_user\(.*?\n.*?return.*?\n',
        r'def get_optional_user\(.*?\n.*?return.*?\n'
    ]

    for pattern in auth_dep_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Clean up extra newlines
    content = re.sub(r'\n\n\n+', '\n\n', content)

    dependencies_path.write_text(content, encoding='utf-8')


def cleanup_dependencies_from_pyproject(project_path: Path, service_type: str, old_provider: str = None) -> None:
    """Remove old service dependencies from pyproject.toml."""
    pyproject_path = project_path / "pyproject.toml"

    if not pyproject_path.exists():
        return

    content = pyproject_path.read_text(encoding='utf-8')

    # Define dependencies to remove based on service type
    dependencies_to_remove = set()

    if service_type == "cache":
        dependencies_to_remove.update([
            "redis", "pymemcache", "boto3", "cachetools"
        ])
    elif service_type == "db":
        dependencies_to_remove.update([
            "sqlalchemy", "psycopg2-binary", "pymysql", "cryptography",
            "motor", "pyodbc"
        ])
    elif service_type == "auth":
        dependencies_to_remove.update([
            "python-jose", "passlib", "authlib", "httpx"
        ])

    # Remove dependencies from the dependencies array
    lines = content.split('\n')
    new_lines = []
    in_dependencies = False

    for line in lines:
        line_stripped = line.strip()

        if line_stripped.startswith('dependencies = ['):
            in_dependencies = True
            new_lines.append(line)
        elif in_dependencies and (line_stripped == ']' or line_stripped.endswith(']')):
            new_lines.append(line)
            in_dependencies = False
        elif in_dependencies:
            # Check if this line contains a dependency to remove
            should_remove = False
            for dep_to_remove in dependencies_to_remove:
                if f'"{dep_to_remove}' in line or f"'{dep_to_remove}" in line:
                    should_remove = True
                    break

            if not should_remove:
                new_lines.append(line)
        else:
            new_lines.append(line)

    pyproject_path.write_text('\n'.join(new_lines), encoding='utf-8')


def cleanup_all_service_files(project_path: Path, service_type: str) -> None:
    """Clean up all files and configurations for a service type."""
    if service_type == "cache":
        cleanup_cache_files(project_path)
        cleanup_cache_config(project_path)
        cleanup_cache_imports(project_path)
    elif service_type == "db":
        cleanup_database_files(project_path)
        cleanup_database_config(project_path)
        cleanup_database_imports(project_path)
    elif service_type == "auth":
        cleanup_auth_files(project_path)
        cleanup_auth_config(project_path)
        cleanup_auth_imports(project_path)
        cleanup_auth_dependencies(project_path)

    # Always clean up dependencies from pyproject.toml
    cleanup_dependencies_from_pyproject(project_path, service_type)


def cleanup_existing_project(project_path: Path) -> None:
    """Clean up an existing project directory before creating a new one.

    This function removes all FastKit-generated files and directories
    to ensure a clean slate for the new project.
    """
    if not project_path.exists():
        return

    import shutil

    # List of directories to remove completely
    dirs_to_remove = [
        "app",
        "tests",
        "infra",
        ".github",
        "services",  # For microservices
        "shared",    # For microservices
        "src",       # For onion architecture (legacy)
        "backend",   # For fullstack
        "frontend"   # For fullstack
    ]

    # List of files to remove
    files_to_remove = [
        "pyproject.toml",
        "README.md",
        ".gitignore",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        "docker-compose.dev.yml",
        "docker-compose.dev.yaml",
        "docker-compose.prod.yml",
        "docker-compose.prod.yaml",
        ".dockerignore"
    ]

    # Remove directories with error handling
    for dir_name in dirs_to_remove:
        dir_path = project_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            try:
                shutil.rmtree(dir_path)
            except (OSError, PermissionError) as e:
                # If we can't remove the directory, try to remove its contents
                try:
                    for item in dir_path.iterdir():
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                except (OSError, PermissionError):
                    # If we still can't remove, skip this directory
                    pass

    # Remove files with error handling
    for file_name in files_to_remove:
        file_path = project_path / file_name
        if file_path.exists() and file_path.is_file():
            try:
                file_path.unlink()
            except (OSError, PermissionError):
                # Skip files we can't remove
                pass

    # Remove any remaining Python cache directories
    try:
        for cache_dir in project_path.rglob("__pycache__"):
            if cache_dir.is_dir():
                try:
                    shutil.rmtree(cache_dir)
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass

    # Remove any .pyc files
    try:
        for pyc_file in project_path.rglob("*.pyc"):
            if pyc_file.is_file():
                try:
                    pyc_file.unlink()
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass

    # Remove any .pyo files
    try:
        for pyo_file in project_path.rglob("*.pyo"):
            if pyo_file.is_file():
                try:
                    pyo_file.unlink()
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
