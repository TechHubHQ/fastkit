"""Domain generator for creating new domains in existing projects."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .dependency_manager import get_dependency_manager


# Initialize Jinja2 environment
_templates_dir = Path(__file__).parent / "templates"
_env = Environment(loader=FileSystemLoader(_templates_dir),
                   trim_blocks=True, lstrip_blocks=True)


def _ensure_dir(path: Path) -> None:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)


def _render_and_write(template_name: str, dest_path: Path, context: dict) -> None:
    """Render template and write to file."""
    template = _env.get_template(template_name)
    content = template.render(context)
    dest_path.write_text(content, encoding='utf-8')


def scaffold_domain(
    project_path: Path,
    domain_name: str,
    with_tests: bool = True,
    force: bool = False
) -> None:
    """Create a new domain in an existing FastKit project."""

    context = {
        "domain_name": domain_name,
        "project_name": project_path.name
    }

    # Create domain directory
    domain_path = project_path / "app" / "domains" / domain_name
    _ensure_dir(domain_path)

    # Create domain files
    domain_files = [
        "__init__.py",
        "models.py",
        "schemas.py",
        "repositories.py",
        "services.py",
        "routes.py",
        "dependencies.py",
        "exceptions.py"
    ]

    for file_name in domain_files:
        template_path = f"domains/{file_name}.jinja"
        dest_path = domain_path / file_name

        if dest_path.exists() and not force:
            continue  # Skip existing files unless force is True

        _render_and_write(template_path, dest_path, context)

    # Create test files if requested
    if with_tests:
        test_domain_path = project_path / "tests" / \
            "domains" / f"test_{domain_name}"
        _ensure_dir(test_domain_path)

        test_files = [
            "__init__.py",
            "test_models.py",
            "test_repositories.py",
            "test_services.py",
            "test_routes.py"
        ]

        for file_name in test_files:
            template_path = f"domains/tests/{file_name}.jinja"
            dest_path = test_domain_path / file_name

            if dest_path.exists() and not force:
                continue  # Skip existing files unless force is True

            # Create basic test templates if they don't exist
            if not (_templates_dir / template_path).exists():
                _create_basic_test_template(dest_path, file_name, context)
            else:
                _render_and_write(template_path, dest_path, context)

    # Detect and sync dependencies based on domain content
    _sync_domain_dependencies(project_path, domain_name)


def _sync_domain_dependencies(project_path: Path, domain_name: str) -> None:
    """Detect and sync dependencies based on domain content."""
    dep_manager = get_dependency_manager(project_path)

    # Check if the project uses a database by looking for existing db services
    app_path = project_path / "app"
    database_detected = False

    # Check for existing database configuration
    config_path = app_path / "core" / "config.py"
    if config_path.exists():
        config_content = config_path.read_text(encoding='utf-8')

        # Detect database type from configuration
        if "postgresql://" in config_content or "psycopg2" in config_content:
            dep_manager.sync_service_dependencies("db", "postgresql")
            database_detected = True
        elif "mysql://" in config_content or "pymysql" in config_content:
            dep_manager.sync_service_dependencies("db", "mysql")
            database_detected = True
        elif "sqlite://" in config_content:
            dep_manager.sync_service_dependencies("db", "sqlite")
            database_detected = True
        elif "mongodb://" in config_content or "motor" in config_content:
            dep_manager.sync_service_dependencies("db", "mongodb")
            database_detected = True
        elif "mssql://" in config_content or "pyodbc" in config_content:
            dep_manager.sync_service_dependencies("db", "mssql")
            database_detected = True

    # Check for existing database directory
    if not database_detected:
        db_path = app_path / "db"
        if db_path.exists():
            # If db directory exists, check what's in it to determine database type
            db_files = list(db_path.glob("*.py"))
            if db_files:
                # Read database files to detect type
                for db_file in db_files:
                    content = db_file.read_text(encoding='utf-8')
                    if "postgresql" in content.lower():
                        dep_manager.sync_service_dependencies(
                            "db", "postgresql")
                        database_detected = True
                        break
                    elif "mysql" in content.lower():
                        dep_manager.sync_service_dependencies("db", "mysql")
                        database_detected = True
                        break
                    elif "mongodb" in content.lower() or "motor" in content.lower():
                        dep_manager.sync_service_dependencies("db", "mongodb")
                        database_detected = True
                        break
                    elif "mssql" in content.lower() or "pyodbc" in content.lower():
                        dep_manager.sync_service_dependencies("db", "mssql")
                        database_detected = True
                        break

    # Check the created domain model to see if it uses SQLAlchemy
    domain_model_path = app_path / "domains" / domain_name / "models.py"
    if domain_model_path.exists():
        model_content = domain_model_path.read_text(encoding='utf-8')
        if "sqlalchemy" in model_content.lower() and not database_detected:
            # Domain uses SQLAlchemy but no specific database detected, default to SQLite
            dep_manager.sync_service_dependencies("db", "sqlite")
            database_detected = True

    # Always add testing dependencies when creating domains with tests
    dep_manager.sync_service_dependencies("testing", "pytest")

    # Add validation dependencies (domains typically use Pydantic schemas)
    dep_manager.sync_service_dependencies("validation", "pydantic")


def _create_basic_test_template(dest_path: Path, file_name: str, context: dict) -> None:
    """Create basic test templates."""
    domain_name = context["domain_name"]

    if file_name == "__init__.py":
        content = f'"""Tests for {domain_name} domain."""'
    elif file_name == "test_models.py":
        content = f'''"""Test {domain_name} models."""

import pytest
from app.domains.{domain_name}.models import {domain_name.title()}


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {{
                "name": "Test {domain_name.title()}",
                "description": "A test {domain_name}",
                "is_active": True
            }},
            {{
                "name": "Test {domain_name.title()}",
                "description": "A test {domain_name}",
                "is_active": True
            }},
        ),
    ],
)
def test_{domain_name}_model_creation(data, expected):
    """Test {domain_name} model creation."""
    obj = {domain_name.title()}(**data)
    assert obj.name == expected["name"]
    assert obj.description == expected["description"]
    assert obj.is_active == expected["is_active"]


def test_{domain_name}_model_repr():
    """Test {domain_name} model string representation."""
    obj = {domain_name.title()}(id=1, name="Test {domain_name.title()}")
    expected = f"<{domain_name.title()}(id=1, name='Test {domain_name.title()}')>"
    assert repr(obj) == expected
'''
    elif file_name == "test_repositories.py":
        content = f'''"""Test {domain_name} repository."""

import pytest
from unittest.mock import Mock
from app.domains.{domain_name}.repositories import {domain_name.title()}Repository
from app.domains.{domain_name}.models import {domain_name.title()}
from app.domains.{domain_name}.schemas import {domain_name.title()}Create, {domain_name.title()}Update


@pytest.fixture
def mock_db():
    """Mock database session."""
    return Mock()


@pytest.fixture
def {domain_name}_repository(mock_db):
    """Create {domain_name} repository with mock db."""
    return {domain_name.title()}Repository(mock_db)


def test_get_{domain_name}({domain_name}_repository, mock_db):
    """Test getting a {domain_name} by ID."""
    # Setup
    mock_{domain_name} = Mock(spec={domain_name.title()})
    mock_db.query.return_value.filter.return_value.first.return_value = mock_{domain_name}

    # Execute
    result = {domain_name}_repository.get(1)

    # Assert
    assert result == mock_{domain_name}
    mock_db.query.assert_called_once_with({domain_name.title()})


def test_create_{domain_name}({domain_name}_repository, mock_db):
    """Test creating a new {domain_name}."""
    # Setup
    {domain_name}_data = {domain_name.title()}Create(
        name="Test {domain_name.title()}",
        description="A test {domain_name}"
    )

    # Execute
    result = {domain_name}_repository.create({domain_name}_data)

    # Assert
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
'''
    elif file_name == "test_services.py":
        content = f'''"""Test {domain_name} service."""

import pytest
from unittest.mock import Mock
from app.domains.{domain_name}.services import {domain_name.title()}Service
from app.domains.{domain_name}.schemas import {domain_name.title()}Create, {domain_name.title()}Response
from app.domains.{domain_name}.exceptions import {domain_name.title()}NotFound, {domain_name.title()}AlreadyExists


@pytest.fixture
def mock_repository():
    """Mock {domain_name} repository."""
    return Mock()


@pytest.fixture
def {domain_name}_service(mock_repository):
    """Create {domain_name} service with mock repository."""
    return {domain_name.title()}Service(mock_repository)


def test_get_{domain_name}_success({domain_name}_service, mock_repository):
    """Test successfully getting a {domain_name}."""
    # Setup
    mock_{domain_name} = Mock()
    mock_{domain_name}.id = 1
    mock_{domain_name}.name = "Test {domain_name.title()}"
    mock_repository.get.return_value = mock_{domain_name}

    # Execute
    result = {domain_name}_service.get_{domain_name}(1)

    # Assert
    assert isinstance(result, {domain_name.title()}Response)
    mock_repository.get.assert_called_once_with(1)


def test_get_{domain_name}_not_found({domain_name}_service, mock_repository):
    """Test getting a {domain_name} that doesn't exist."""
    # Setup
    mock_repository.get.return_value = None

    # Execute & Assert
    with pytest.raises({domain_name.title()}NotFound):
        {domain_name}_service.get_{domain_name}(999)


def test_create_{domain_name}_success({domain_name}_service, mock_repository):
    """Test successfully creating a {domain_name}."""
    # Setup
    {domain_name}_data = {domain_name.title()}Create(
        name="New {domain_name.title()}",
        description="A new {domain_name}"
    )
    mock_repository.get_by_name.return_value = None  # No existing {domain_name}
    mock_{domain_name} = Mock()
    mock_repository.create.return_value = mock_{domain_name}

    # Execute
    result = {domain_name}_service.create_{domain_name}({domain_name}_data)

    # Assert
    assert isinstance(result, {domain_name.title()}Response)
    mock_repository.create.assert_called_once_with({domain_name}_data)


def test_create_{domain_name}_already_exists({domain_name}_service, mock_repository):
    """Test creating a {domain_name} that already exists."""
    # Setup
    {domain_name}_data = {domain_name.title()}Create(
        name="Existing {domain_name.title()}",
        description="An existing {domain_name}"
    )
    mock_repository.get_by_name.return_value = Mock()  # Existing {domain_name}

    # Execute & Assert
    with pytest.raises({domain_name.title()}AlreadyExists):
        {domain_name}_service.create_{domain_name}({domain_name}_data)
'''
    elif file_name == "test_routes.py":
        content = f'''"""Test {domain_name} routes."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


def test_get_all_{domain_name}(client):
    """Test getting all {domain_name} records."""
    response = client.get("/api/v1/{domain_name}/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_{domain_name}_by_id(client):
    """Test getting a {domain_name} by ID."""
    # This test will need to be updated based on your actual implementation
    # For now, it just tests that the endpoint exists
    response = client.get("/api/v1/{domain_name}/1")

    # The response might be 404 if no {domain_name} exists, which is fine for this test
    assert response.status_code in [200, 404]


def test_create_{domain_name}(client):
    """Test creating a new {domain_name}."""
    {domain_name}_data = {{
        "name": "Test {domain_name.title()}",
        "description": "A test {domain_name}",
        "is_active": True
    }}

    response = client.post("/api/v1/{domain_name}/create", json={domain_name}_data)

    # The response might vary based on your implementation
    # This test just ensures the endpoint is accessible
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.parametrize("invalid_data", [
    {{}},  # Empty data
    {{'name': ''}},  # Empty name
    {{'description': 'No name'}},  # Missing name
])
def test_create_{domain_name}_invalid_data(client, invalid_data):
    """Test creating a {domain_name} with invalid data."""
    response = client.post("/api/v1/{domain_name}/create", json=invalid_data)

    assert response.status_code == 422  # Validation error
'''
    else:
        content = f'"""Test {file_name.replace(".py", "").replace("test_", "")} for {domain_name} domain."""'

    dest_path.write_text(content, encoding='utf-8')
