"""Dependency management for FastKit projects."""

import re
from pathlib import Path
from typing import Dict, List, Set


class DependencyManager:
    """Manages project dependencies and syncs them with pyproject.toml."""

    # Define all possible dependencies for different services/components
    DEPENDENCIES = {
        # Database dependencies
        "db": {
            "postgresql": ["sqlalchemy>=2.0.0", "psycopg2-binary>=2.9.0"],
            "mysql": ["sqlalchemy>=2.0.0", "pymysql>=1.0.0"],
            "sqlite": ["sqlalchemy>=2.0.0"],
            "mongodb": ["motor>=3.0.0"],
            "mssql": ["sqlalchemy>=2.0.0", "pyodbc>=4.0.0"],
        },

        # Cache dependencies
        "cache": {
            "redis": ["redis>=4.0.0"],
            "memcached": ["pymemcache>=4.0.0"],
            "dynamodb": ["boto3>=1.26.0"],
            "in-memory": ["cachetools>=5.0.0"],
        },

        # Auth dependencies
        "auth": {
            "jwt": ["python-jose[cryptography]>=3.3.0", "passlib[bcrypt]>=1.7.4"],
            "oauth": ["authlib>=1.2.0", "httpx>=0.24.0"],
        },

        # API dependencies
        "api": {
            "rest": ["fastapi>=0.116", "uvicorn[standard]>=0.30"],
            "graphql": ["strawberry-graphql>=0.200.0"],
            "websocket": ["websockets>=11.0.0"],
        },

        # Testing dependencies
        "testing": {
            "pytest": ["pytest>=7.0.0", "pytest-asyncio>=0.21.0"],
            "coverage": ["pytest-cov>=4.0.0"],
            "factory": ["factory-boy>=3.2.0"],
            "mock": ["pytest-mock>=3.10.0"],
        },

        # Validation dependencies
        "validation": {
            "pydantic": ["pydantic>=2.0.0", "pydantic-settings>=2.0.0"],
            "marshmallow": ["marshmallow>=3.19.0"],
        },

        # Serialization dependencies
        "serialization": {
            "json": [],  # Built-in
            "yaml": ["PyYAML>=6.0"],
            "xml": ["lxml>=4.9.0"],
            "msgpack": ["msgpack>=1.0.0"],
        },

        # HTTP client dependencies
        "http": {
            "requests": ["requests>=2.28.0"],
            "httpx": ["httpx>=0.24.0"],
            "aiohttp": ["aiohttp>=3.8.0"],
        },

        # Background task dependencies
        "tasks": {
            "celery": ["celery>=5.2.0", "redis>=4.0.0"],
            "rq": ["rq>=1.13.0", "redis>=4.0.0"],
            "dramatiq": ["dramatiq>=1.13.0", "redis>=4.0.0"],
        },

        # Job scheduler dependencies
        "jobs": {
            "celery": ["celery>=5.2.0", "redis>=4.0.0"],
            "rq": ["rq>=1.13.0", "redis>=4.0.0"],
            "apscheduler": ["apscheduler>=3.10.0"],
            "dramatiq": ["dramatiq>=1.13.0", "redis>=4.0.0"],
            "arq": ["arq>=0.25.0", "redis>=4.0.0"],
        },

        # Monitoring dependencies
        "monitoring": {
            "prometheus": ["prometheus-client>=0.16.0"],
            "sentry": ["sentry-sdk>=1.15.0"],
            "logging": ["structlog>=22.3.0"],
        },

        # Security dependencies
        "security": {
            "cors": ["fastapi-cors>=0.0.6"],
            "rate-limiting": ["slowapi>=0.1.8"],
            "encryption": ["cryptography>=40.0.0"],
        },

        # File handling dependencies
        "files": {
            "images": ["Pillow>=9.5.0"],
            "pdf": ["PyPDF2>=3.0.0"],
            "excel": ["openpyxl>=3.1.0"],
            "csv": [],  # Built-in
        },

        # Cloud dependencies
        "cloud": {
            "aws": ["boto3>=1.26.0"],
            "gcp": ["google-cloud-storage>=2.8.0"],
            "azure": ["azure-storage-blob>=12.14.0"],
        },

        # Message queue dependencies
        "messaging": {
            "rabbitmq": ["pika>=1.3.0"],
            "kafka": ["kafka-python>=2.0.2"],
            "redis-pubsub": ["redis>=4.0.0"],
        },
    }

    def __init__(self, project_path: Path):
        """Initialize dependency manager with project path."""
        self.project_path = project_path
        self.pyproject_path = project_path / "pyproject.toml"

    def get_dependencies_for_service(self, service_type: str, service_provider: str) -> List[str]:
        """Get dependencies for a specific service type and provider."""
        if service_type in self.DEPENDENCIES:
            return self.DEPENDENCIES[service_type].get(service_provider, [])
        return []

    def get_dependencies_for_component(self, component_type: str, component_name: str) -> List[str]:
        """Get dependencies for a specific component."""
        return self.get_dependencies_for_service(component_type, component_name)

    def read_current_dependencies(self) -> Set[str]:
        """Read current dependencies from pyproject.toml."""
        if not self.pyproject_path.exists():
            return set()

        content = self.pyproject_path.read_text(encoding='utf-8')
        dependencies = set()

        # Extract dependencies from the dependencies array
        in_dependencies = False
        for line in content.split('\n'):
            line = line.strip()
            if line == 'dependencies = [':
                in_dependencies = True
                continue
            elif in_dependencies and line == ']':
                break
            elif in_dependencies and line.startswith('"') and line.endswith('",'):
                # Extract dependency name (remove quotes and comma)
                dep = line[1:-2]
                dependencies.add(dep)

        return dependencies

    def add_dependencies(self, new_dependencies: List[str]) -> bool:
        """Add new dependencies to pyproject.toml."""
        if not new_dependencies or not self.pyproject_path.exists():
            return False

        current_deps = self.read_current_dependencies()

        # Filter out dependencies that already exist
        deps_to_add = []
        for dep in new_dependencies:
            # Extract package name (before >= or ==)
            package_name = re.split(r'[><=!]', dep)[0].strip()

            # Check if this package is already in dependencies
            already_exists = any(
                re.split(r'[><=!]', existing_dep)[0].strip() == package_name
                for existing_dep in current_deps
            )

            if not already_exists:
                deps_to_add.append(dep)

        if not deps_to_add:
            return True  # Nothing to add

        # Read the current file content
        content = self.pyproject_path.read_text(encoding='utf-8')

        # Find the dependencies section and add new dependencies
        lines = content.split('\n')
        new_lines = []
        in_dependencies = False

        for line in lines:
            if line.strip() == 'dependencies = [':
                in_dependencies = True
                new_lines.append(line)
            elif in_dependencies and line.strip() == ']':
                # Add new dependencies before the closing bracket
                for dep in deps_to_add:
                    new_lines.append(f'    "{dep}",')
                new_lines.append(line)
                in_dependencies = False
            else:
                new_lines.append(line)

        # Write the updated content back
        self.pyproject_path.write_text('\n'.join(new_lines), encoding='utf-8')
        return True

    def sync_service_dependencies(self, service_type: str, service_provider: str) -> bool:
        """Sync dependencies for a specific service."""
        dependencies = self.get_dependencies_for_service(
            service_type, service_provider)
        return self.add_dependencies(dependencies)

    def sync_multiple_services(self, services: Dict[str, str]) -> bool:
        """Sync dependencies for multiple services at once."""
        all_dependencies = []

        for service_type, service_provider in services.items():
            deps = self.get_dependencies_for_service(
                service_type, service_provider)
            all_dependencies.extend(deps)

        return self.add_dependencies(all_dependencies)

    def remove_dependencies(self, dependencies_to_remove: List[str]) -> bool:
        """Remove dependencies from pyproject.toml."""
        if not dependencies_to_remove or not self.pyproject_path.exists():
            return False

        # Extract package names to remove
        packages_to_remove = set()
        for dep in dependencies_to_remove:
            package_name = re.split(r'[><=!]', dep)[0].strip()
            packages_to_remove.add(package_name)

        # Read the current file content
        content = self.pyproject_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        new_lines = []
        in_dependencies = False

        for line in lines:
            if line.strip() == 'dependencies = [':
                in_dependencies = True
                new_lines.append(line)
            elif in_dependencies and line.strip() == ']':
                new_lines.append(line)
                in_dependencies = False
            elif in_dependencies and line.strip().startswith('"') and line.strip().endswith('",'):
                # Check if this dependency should be removed
                dep = line.strip()[1:-2]  # Remove quotes and comma
                package_name = re.split(r'[><=!]', dep)[0].strip()

                if package_name not in packages_to_remove:
                    new_lines.append(line)
                # If package should be removed, don't add the line
            else:
                new_lines.append(line)

        # Write the updated content back
        self.pyproject_path.write_text('\n'.join(new_lines), encoding='utf-8')
        return True


def get_dependency_manager(project_path: Path) -> DependencyManager:
    """Get a dependency manager instance for the given project path."""
    return DependencyManager(project_path)
