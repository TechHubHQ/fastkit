"""Cache generator for unified cache setup across project creation and service addition."""

from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader

from .utils import ensure_dir, render_and_write
from .cleanup_utils import cleanup_cache_files, cleanup_cache_config, cleanup_cache_imports


def generate_cache_setup(
    project_path: Path,
    cache_choice: str,
    project_name: str,
    template_env: Environment = None,
    clean_existing: bool = True
) -> None:
    """Generate unified cache setup files.

    This function ensures consistent cache generation whether called during
    project creation or service addition.

    Args:
        project_path: Path to the project root
        cache_choice: Cache choice (redis, memcached, dynamodb, in-memory, none)
        project_name: Name of the project
        template_env: Optional Jinja2 environment (will create if not provided)
        clean_existing: Whether to clean up existing cache files before generating new ones
    """
    # Clean up existing cache setup if requested
    if clean_existing:
        cleanup_cache_files(project_path)
        cleanup_cache_config(project_path)
        cleanup_cache_imports(project_path)
    
    if cache_choice == "none":
        return

    # Initialize Jinja2 environment if not provided
    if template_env is None:
        templates_dir = Path(__file__).parent / "templates"
        template_env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=False,
            lstrip_blocks=False
        )

    # Create cache directory
    cache_dir = project_path / "app" / "cache"
    ensure_dir(cache_dir)

    # Context for template rendering
    context = {
        "cache_choice": cache_choice,
        "project_name": project_name
    }

    # Generate core cache files
    _generate_core_cache_files(cache_dir, context, template_env)

    # Generate cache-specific client files
    _generate_cache_client_files(
        cache_dir, cache_choice, context, template_env)


def _generate_core_cache_files(
    cache_dir: Path,
    context: Dict[str, Any],
    template_env: Environment
) -> None:
    """Generate core cache files that are common across all cache types."""

    # Generate __init__.py
    render_and_write(
        "services/cache/__init__.py.jinja",
        cache_dir / "__init__.py",
        context,
        template_env
    )


def _generate_cache_client_files(
    cache_dir: Path,
    cache_choice: str,
    context: Dict[str, Any],
    template_env: Environment
) -> None:
    """Generate cache-specific client files."""

    # Map cache choices to their client template files
    client_templates = {
        "redis": "services/cache/redis_client.py.jinja",
        "memcached": "services/cache/memcached_client.py.jinja",
        "dynamodb": "services/cache/dynamodb_client.py.jinja",
        "in-memory": "services/cache/memory_client.py.jinja"
    }

    # Map cache choices to their client file names
    client_files = {
        "redis": "redis_client.py",
        "memcached": "memcached_client.py",
        "dynamodb": "dynamodb_client.py",
        "in-memory": "memory_client.py"
    }

    if cache_choice in client_templates:
        render_and_write(
            client_templates[cache_choice],
            cache_dir / client_files[cache_choice],
            context,
            template_env
        )


def update_cache_configuration(
    project_path: Path,
    cache_choice: str,
    project_name: str
) -> None:
    """Update configuration files with cache settings.

    This ensures that the app configuration is updated with the appropriate
    cache connection settings.
    """
    if cache_choice == "none":
        return

    config_path = project_path / "app" / "core" / "config.py"
    if not config_path.exists():
        return

    content = config_path.read_text(encoding='utf-8')

    # Check if cache settings already exist
    if "# Cache settings" in content:
        return

    # Generate cache configuration
    cache_config = _generate_cache_config_section(cache_choice, project_name)

    # Insert cache configuration before the Config class
    if "class Config:" in content:
        content = content.replace(
            "    class Config:",
            f"{cache_config}\n    class Config:"
        )
        config_path.write_text(content, encoding='utf-8')


def _generate_cache_config_section(cache_choice: str, project_name: str) -> str:
    """Generate cache configuration section for config.py."""

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


def ensure_cache_imports_in_main(project_path: Path, cache_choice: str) -> None:
    """Ensure cache imports are properly set up in main.py."""
    if cache_choice == "none":
        return

    main_path = project_path / "app" / "main.py"
    if not main_path.exists():
        return

    content = main_path.read_text(encoding='utf-8')

    # Check if cache imports already exist
    if "from app.cache" in content:
        return

    # Add cache imports after other imports
    import_line = "from app.cache import cache_client"

    # Find the last import line and add after it
    lines = content.split('\n')
    last_import_index = -1

    for i, line in enumerate(lines):
        if line.strip().startswith('from ') or line.strip().startswith('import '):
            last_import_index = i

    if last_import_index >= 0:
        lines.insert(last_import_index + 1, import_line)
        content = '\n'.join(lines)
        main_path.write_text(content, encoding='utf-8')
