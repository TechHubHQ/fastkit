"""Database generator for unified database setup across project creation and service addition."""

from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader

from .utils import ensure_dir, render_and_write


def generate_database_setup(
    project_path: Path,
    db_choice: str,
    project_name: str,
    template_env: Environment = None
) -> None:
    """Generate unified database setup files.

    This function ensures consistent database generation whether called during
    project creation or service addition.

    Args:
        project_path: Path to the project root
        db_choice: Database choice (postgresql, mysql, sqlite, mongodb, mssql, none)
        project_name: Name of the project
        template_env: Optional Jinja2 environment (will create if not provided)
    """
    if db_choice == "none":
        return

    # Initialize Jinja2 environment if not provided
    if template_env is None:
        templates_dir = Path(__file__).parent / "templates"
        template_env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=False,
            lstrip_blocks=False
        )

    # Create database directory
    db_dir = project_path / "app" / "db"
    ensure_dir(db_dir)

    # Context for template rendering
    context = {
        "db_choice": db_choice,
        "project_name": project_name
    }

    # Generate core database files
    _generate_core_db_files(db_dir, context, template_env)

    # Generate database-specific client files
    _generate_db_client_files(db_dir, db_choice, context, template_env)


def _generate_core_db_files(
    db_dir: Path,
    context: Dict[str, Any],
    template_env: Environment
) -> None:
    """Generate core database files that are common across all database types."""

    # Generate __init__.py
    render_and_write(
        "services/db/__init__.py.jinja",
        db_dir / "__init__.py",
        context,
        template_env
    )

    # Generate base.py (connection and engine setup)
    render_and_write(
        "services/db/base.py.jinja",
        db_dir / "base.py",
        context,
        template_env
    )

    # Generate session.py (session management and database manager)
    render_and_write(
        "services/db/session.py.jinja",
        db_dir / "session.py",
        context,
        template_env
    )

    # Generate base_model.py (model definitions and mixins)
    render_and_write(
        "services/db/base_model.py.jinja",
        db_dir / "base_model.py",
        context,
        template_env
    )


def _generate_db_client_files(
    db_dir: Path,
    db_choice: str,
    context: Dict[str, Any],
    template_env: Environment
) -> None:
    """Generate database-specific client files."""

    # Map database choices to their client template files
    client_templates = {
        "postgresql": "services/db/postgresql_client.py.jinja",
        "mysql": "services/db/mysql_client.py.jinja",
        "sqlite": "services/db/sqlite_client.py.jinja",
        "mongodb": "services/db/mongodb_client.py.jinja",
        "mssql": "services/db/mssql_client.py.jinja"
    }

    # Map database choices to their client file names
    client_files = {
        "postgresql": "postgresql_client.py",
        "mysql": "mysql_client.py",
        "sqlite": "sqlite_client.py",
        "mongodb": "mongodb_client.py",
        "mssql": "mssql_client.py"
    }

    if db_choice in client_templates:
        render_and_write(
            client_templates[db_choice],
            db_dir / client_files[db_choice],
            context,
            template_env
        )


def update_database_configuration(
    project_path: Path,
    db_choice: str,
    project_name: str
) -> None:
    """Update configuration files with database settings.

    This ensures that the app configuration is updated with the appropriate
    database connection settings.
    """
    if db_choice == "none":
        return

    config_path = project_path / "app" / "core" / "config.py"
    if not config_path.exists():
        return

    content = config_path.read_text(encoding='utf-8')

    # Check if database settings already exist
    if "# Database settings" in content:
        return

    # Generate database configuration
    db_config = _generate_database_config_section(db_choice, project_name)

    # Insert database configuration before the Config class
    if "class Config:" in content:
        content = content.replace(
            "    class Config:",
            f"{db_config}\n    class Config:"
        )
        config_path.write_text(content, encoding='utf-8')


def _generate_database_config_section(db_choice: str, project_name: str) -> str:
    """Generate database configuration section for config.py."""

    db_configs = {
        "postgresql": f'''    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/{project_name.replace("-", "_")}_db")''',
        "mysql": f'''    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql://user:password@localhost/{project_name.replace("-", "_")}_db")''',
        "sqlite": f'''    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./{project_name.replace("-", "_")}.db")''',
        "mongodb": f'''    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mongodb://localhost:27017/{project_name.replace("-", "_")}_db")''',
        "mssql": f'''    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mssql://user:password@localhost/{project_name.replace("-", "_")}_db")'''
    }

    return db_configs.get(db_choice, "")


def ensure_database_imports_in_main(project_path: Path, db_choice: str) -> None:
    """Ensure database imports are properly set up in main.py."""
    if db_choice == "none":
        return

    main_path = project_path / "app" / "main.py"
    if not main_path.exists():
        return

    content = main_path.read_text(encoding='utf-8')

    # Check if database imports already exist
    if "from app.db" in content:
        return

    # Add database imports after other imports
    import_line = "from app.db.session import db_manager"

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
