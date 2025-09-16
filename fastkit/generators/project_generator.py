from pathlib import Path
from typing import Literal
from jinja2 import Environment, FileSystemLoader


AuthType = Literal["none", "jwt", "oauth"]
ArchitectureType = Literal["fullstack",
                           "microservices", "rest-apis", "onion-architecture"]
DbType = Literal["none", "postgresql", "sqlite", "mysql", "mongodb", "mssql"]
CacheType = Literal["none", "redis"]


# Initialize Jinja2 environment
_templates_dir = Path(__file__).parent / "templates"
_env = Environment(loader=FileSystemLoader(_templates_dir),
                   trim_blocks=True, lstrip_blocks=True)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _render_and_write(template_name: str, dest_path: Path, context: dict) -> None:
    template = _env.get_template(template_name)
    content = template.render(context)
    dest_path.write_text(content)


def _scaffold_service(service_path: Path, service_name: str, auth_type: AuthType, db_choice: DbType, cache_choice: CacheType) -> None:
    src_app = service_path / "app"
    api_dir = src_app / "api"
    v1_dir = api_dir / "v1"
    core_dir = src_app / "core"
    models_dir = src_app / "models"
    services_dir = src_app / "services"
    repositories_dir = src_app / "repositories"
    db_dir = src_app / "db"
    auth_dir = src_app / "auth"
    cache_dir = src_app / "cache"
    tests_dir = service_path / "tests"
    infra_dir = service_path / "infra"

    for d in [
        service_path,
        src_app,
        api_dir,
        v1_dir,
        core_dir,
        models_dir,
        services_dir,
        repositories_dir,
        tests_dir,
        infra_dir,
    ]:
        _ensure_dir(d)

    if auth_type != "none":
        _ensure_dir(auth_dir)
        _render_and_write("service/app/auth/__init__.py.jinja", auth_dir / "__init__.py", {})
        _render_and_write("service/app/auth/routes.py.jinja", auth_dir / "routes.py", {})

    if db_choice != "none":
        _ensure_dir(db_dir)
        _render_and_write("service/app/db/__init__.py.jinja", db_dir / "__init__.py", {})
        _render_and_write("service/app/db/session.py.jinja", db_dir / "session.py", {})

    if cache_choice != "none":
        _ensure_dir(cache_dir)
        _render_and_write("service/app/cache/__init__.py.jinja", cache_dir / "__init__.py", {})
        _render_and_write("service/app/cache/client.py.jinja", cache_dir / "client.py", {})

    _render_and_write("service/app/__init__.py.jinja", src_app / "__init__.py", {})
    _render_and_write("service/app/main.py.jinja", src_app / "main.py", {"title": service_name})
    _render_and_write("service/app/core/__init__.py.jinja", core_dir / "__init__.py", {})
    _render_and_write("service/app/core/config.py.jinja", core_dir / "config.py", {})
    _render_and_write("service/app/api/__init__.py.jinja", api_dir / "__init__.py", {})
    _render_and_write("service/app/api/v1/__init__.py.jinja", v1_dir / "__init__.py", {})
    _render_and_write("service/app/api/v1/routes.py.jinja", v1_dir / "routes.py", {})
    _render_and_write("service/app/models/__init__.py.jinja", models_dir / "__init__.py", {})
    _render_and_write("service/app/services/__init__.py.jinja", services_dir / "__init__.py", {})
    _render_and_write("service/app/repositories/__init__.py.jinja", repositories_dir / "__init__.py", {})
    _render_and_write("service/tests/__init__.py.jinja", tests_dir / "__init__.py", {})
    _render_and_write("service/infra/.gitkeep.jinja", infra_dir / ".gitkeep", {})


def scaffold_project_structure(
    *,
    base_path: Path,
    project_name: str,
    architecture: ArchitectureType = "rest-apis",
    auth_type: AuthType = "none",
    db_choice: DbType = "none",
    cache_choice: CacheType = "none",
) -> None:
    """Create a best-practice FastAPI project directory structure.

    This function only creates directories and minimal placeholder files.
    No integrations are configured; we merely reflect the user's selections
    in the structure.
    """

    app_root = base_path
    # Ensure the root project directory exists
    _ensure_dir(app_root)

    if architecture == "rest-apis":
        _scaffold_service(app_root, project_name, auth_type,
                          db_choice, cache_choice)

    elif architecture == "fullstack":
        # Handle Fullstack architecture
        # Backend part (similar to rest-apis)
        backend_root = app_root / "backend"
        _scaffold_service(backend_root, project_name,
                          auth_type, db_choice, cache_choice)

        # Frontend part
        frontend_root = app_root / "frontend"
        frontend_src = frontend_root / "src"
        _ensure_dir(frontend_root)
        _ensure_dir(frontend_src)
        _render_and_write("project/fullstack/frontend/src/main.ts.jinja", frontend_src / "main.ts", {})
        _render_and_write("project/fullstack/frontend/package.json.jinja", frontend_root / "package.json", {"project_name": project_name})
        _render_and_write("project/fullstack/frontend/tsconfig.json.jinja", frontend_root / "tsconfig.json", {})

    elif architecture == "microservices":
        # Handle Microservices architecture
        services_root = app_root / "services"
        _ensure_dir(services_root)
        service_names = ["service1", "service2"]  # Example services
        for service_name in service_names:
            service_path = services_root / service_name
            _scaffold_service(service_path, service_name,
                              auth_type, db_choice, cache_choice)

    elif architecture == "onion-architecture":
        # Handle Onion architecture
        application_dir = app_root / "application"
        domain_dir = app_root / "domain"
        infrastructure_dir = app_root / "infrastructure"
        presentation_dir = app_root / "presentation"

        for d in [application_dir, domain_dir, infrastructure_dir, presentation_dir]:
            _ensure_dir(d)

        # Create __init__.py files
        _render_and_write("service/app/__init__.py.jinja", application_dir / "__init__.py", {})
        _render_and_write("service/app/__init__.py.jinja", domain_dir / "__init__.py", {})
        _render_and_write("service/app/__init__.py.jinja", infrastructure_dir / "__init__.py", {})
        _render_and_write("service/app/__init__.py.jinja", presentation_dir / "__init__.py", {})

    # UV/pyproject setup and top-level files
    _render_and_write("project/pyproject.toml.jinja", app_root / "pyproject.toml", {"project_name": project_name})
    _render_and_write("project/README.md.jinja", app_root / "README.md", {"project_name": project_name})
    _render_and_write("project/.gitignore.jinja", app_root / ".gitignore", {})
