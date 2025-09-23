"""Auth generator for unified authentication setup across project creation and service addition."""

from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader

from .utils import ensure_dir, render_and_write


def generate_auth_setup(
    project_path: Path,
    auth_type: str,
    project_name: str,
    template_env: Environment = None
) -> None:
    """Generate unified auth setup files.

    This function ensures consistent auth generation whether called during
    project creation or service addition.

    Args:
        project_path: Path to the project root
        auth_type: Auth type (jwt, oauth, none)
        project_name: Name of the project
        template_env: Optional Jinja2 environment (will create if not provided)
    """
    if auth_type == "none":
        return

    # Initialize Jinja2 environment if not provided
    if template_env is None:
        templates_dir = Path(__file__).parent / "templates"
        template_env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=False,
            lstrip_blocks=False
        )

    # Create auth directory
    auth_dir = project_path / "app" / "auth"
    ensure_dir(auth_dir)

    # Context for template rendering
    context = {
        "auth_type": auth_type,
        "project_name": project_name
    }

    # Generate core auth files
    _generate_core_auth_files(auth_dir, context, template_env)

    # Generate auth-specific provider files
    _generate_auth_provider_files(auth_dir, auth_type, context, template_env)


def _generate_core_auth_files(
    auth_dir: Path,
    context: Dict[str, Any],
    template_env: Environment
) -> None:
    """Generate core auth files that are common across all auth types."""

    # Generate __init__.py
    render_and_write(
        "services/auth/__init__.py.jinja",
        auth_dir / "__init__.py",
        context,
        template_env
    )


def _generate_auth_provider_files(
    auth_dir: Path,
    auth_type: str,
    context: Dict[str, Any],
    template_env: Environment
) -> None:
    """Generate auth-specific provider files."""

    # Map auth types to their provider template files
    provider_templates = {
        "jwt": "services/auth/jwt_provider.py.jinja",
        "oauth": "services/auth/oauth_provider.py.jinja"
    }

    # Map auth types to their provider file names
    provider_files = {
        "jwt": "jwt_provider.py",
        "oauth": "oauth_provider.py"
    }

    if auth_type in provider_templates:
        render_and_write(
            provider_templates[auth_type],
            auth_dir / provider_files[auth_type],
            context,
            template_env
        )


def update_auth_configuration(
    project_path: Path,
    auth_type: str,
    project_name: str
) -> None:
    """Update configuration files with auth settings.

    This ensures that the app configuration is updated with the appropriate
    authentication settings.
    """
    if auth_type == "none":
        return

    config_path = project_path / "app" / "core" / "config.py"
    if not config_path.exists():
        return

    content = config_path.read_text(encoding='utf-8')

    # Check if auth settings already exist
    if "# Authentication settings" in content:
        return

    # Generate auth configuration
    auth_config = _generate_auth_config_section(auth_type, project_name)

    # Insert auth configuration before the Config class
    if "class Config:" in content:
        content = content.replace(
            "    class Config:",
            f"{auth_config}\n    class Config:"
        )
        config_path.write_text(content, encoding='utf-8')


def _generate_auth_config_section(auth_type: str, project_name: str) -> str:
    """Generate auth configuration section for config.py."""

    auth_configs = {
        "jwt": '''    # Authentication settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))''',
        "oauth": '''    # Authentication settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    OAUTH_CLIENT_ID: str = os.getenv("OAUTH_CLIENT_ID", "")
    OAUTH_CLIENT_SECRET: str = os.getenv("OAUTH_CLIENT_SECRET", "")
    OAUTH_REDIRECT_URI: str = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8000/auth/callback")
    OAUTH_PROVIDER_URL: str = os.getenv("OAUTH_PROVIDER_URL", "https://accounts.google.com")'''
    }

    return auth_configs.get(auth_type, "")


def ensure_auth_imports_in_main(project_path: Path, auth_type: str) -> None:
    """Ensure auth imports are properly set up in main.py."""
    if auth_type == "none":
        return

    main_path = project_path / "app" / "main.py"
    if not main_path.exists():
        return

    content = main_path.read_text(encoding='utf-8')

    # Check if auth imports already exist
    if "from app.auth" in content:
        return

    # Add auth imports after other imports
    import_line = "from app.auth import auth_service"

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


def generate_auth_dependencies(project_path: Path, auth_type: str) -> None:
    """Generate auth dependency functions for FastAPI dependency injection."""
    if auth_type == "none":
        return

    # Create dependencies file if it doesn't exist
    dependencies_path = project_path / "app" / "core" / "dependencies.py"
    if not dependencies_path.exists():
        return

    content = dependencies_path.read_text(encoding='utf-8')

    # Check if auth dependencies already exist
    if "get_current_user" in content:
        return

    # Add auth dependencies
    auth_dependencies = _generate_auth_dependencies_code(auth_type)

    # Append to the file
    content += "\n\n" + auth_dependencies
    dependencies_path.write_text(content, encoding='utf-8')


def _generate_auth_dependencies_code(auth_type: str) -> str:
    """Generate auth dependency injection code."""

    if auth_type == "jwt":
        return '''# Authentication dependencies
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import auth_service

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    payload = auth_service.verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"user_id": user_id, "payload": payload}


def get_optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user if authenticated, None otherwise."""
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None'''

    elif auth_type == "oauth":
        return '''# Authentication dependencies
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import auth_service

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user from OAuth token."""
    token = credentials.credentials
    user_info = auth_service.verify_token(token)

    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_info


def get_optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user if authenticated, None otherwise."""
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None'''

    return ""
