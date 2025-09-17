from pathlib import Path
from typing import Literal
from jinja2 import Environment, FileSystemLoader


AuthType = Literal["none", "jwt", "oauth"]
ArchitectureType = Literal["fullstack",
                           "microservices", "rest-apis", "onion-architecture"]
DbType = Literal["none", "postgresql", "sqlite", "mysql", "mongodb", "mssql"]
CacheType = Literal["none", "redis"]
FrontendFramework = Literal["react", "angular", "vue", "vanilla"]
BuildTool = Literal["vite", "webpack", "create-react-app", "angular-cli"]
LanguageType = Literal["typescript", "javascript"]


# Initialize Jinja2 environment
_templates_dir = Path(__file__).parent / "templates"
_env = Environment(loader=FileSystemLoader(_templates_dir),
                   trim_blocks=True, lstrip_blocks=True)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _render_and_write(template_name: str, dest_path: Path, context: dict) -> None:
    template = _env.get_template(template_name)
    content = template.render(context)
    dest_path.write_text(content, encoding='utf-8')


def _scaffold_microservices(base_path: Path, project_name: str, auth_type: AuthType, db_choice: DbType, cache_choice: CacheType, config: dict) -> None:
    """Scaffold a microservices architecture."""
    services_root = base_path / "services"
    shared_root = base_path / "shared"
    
    _ensure_dir(services_root)
    _ensure_dir(shared_root)
    
    # Create shared libraries
    if config.get("include_shared", True):
        shared_models = shared_root / "models"
        shared_utils = shared_root / "utils"
        shared_auth = shared_root / "auth"
        
        for d in [shared_models, shared_utils, shared_auth]:
            _ensure_dir(d)
            _render_and_write("service/app/__init__.py.jinja", d / "__init__.py", {})
    
    # Create API Gateway if requested
    if config.get("include_gateway", True):
        gateway_path = services_root / "api-gateway"
        _scaffold_service(gateway_path, "api-gateway", auth_type, db_choice, cache_choice)
        
        # Create gateway-specific files
        gateway_config = gateway_path / "app" / "gateway"
        _ensure_dir(gateway_config)
        _render_and_write("project/microservices/gateway/routes.py.jinja", 
                         gateway_config / "routes.py", {"services": config.get("services", [])})
    
    # Create individual services
    for service_name in config.get("services", ["service-1", "service-2"]):
        service_path = services_root / service_name
        _scaffold_service(service_path, service_name, auth_type, db_choice, cache_choice)
    
    # Create docker-compose for orchestration
    services_list = config.get("services", [])
    if config.get("include_gateway", True):
        services_list = ["api-gateway"] + services_list
    
    _render_and_write("project/microservices/docker-compose.yml.jinja", 
                     base_path / "docker-compose.yml", 
                     {"services": services_list, "project_name": project_name})
    
    _render_and_write("project/microservices/docker-compose.dev.yml.jinja", 
                     base_path / "docker-compose.dev.yml", 
                     {"services": services_list, "project_name": project_name})


def _scaffold_onion_architecture(base_path: Path, project_name: str, auth_type: AuthType, db_choice: DbType, cache_choice: CacheType, config: dict) -> None:
    """Scaffold an onion architecture."""
    src_root = base_path / "src"
    
    # Create main layers
    domain_dir = src_root / "domain"
    application_dir = src_root / "application"
    infrastructure_dir = src_root / "infrastructure"
    presentation_dir = src_root / "presentation"
    
    _ensure_dir(src_root)
    
    # Domain layer
    domain_entities = domain_dir / "entities"
    domain_value_objects = domain_dir / "value_objects"
    domain_repositories = domain_dir / "repositories"
    domain_services = domain_dir / "services"
    
    for d in [domain_entities, domain_value_objects, domain_repositories, domain_services]:
        _ensure_dir(d)
        _render_and_write("service/app/__init__.py.jinja", d / "__init__.py", {})
    
    # Create entity files for each configured entity
    entities = config.get("entities", ["User", "Product"])
    for entity in entities:
        _render_and_write("project/onion/domain/entity.py.jinja", 
                         domain_entities / f"{entity.lower()}.py", 
                         {"entity_name": entity})
    
    # Application layer
    app_use_cases = application_dir / "use_cases"
    app_dtos = application_dir / "dtos"
    app_interfaces = application_dir / "interfaces"
    
    if config.get("include_cqrs", False):
        app_commands = application_dir / "commands"
        app_queries = application_dir / "queries"
        for d in [app_use_cases, app_dtos, app_interfaces, app_commands, app_queries]:
            _ensure_dir(d)
            _render_and_write("service/app/__init__.py.jinja", d / "__init__.py", {})
    else:
        for d in [app_use_cases, app_dtos, app_interfaces]:
            _ensure_dir(d)
            _render_and_write("service/app/__init__.py.jinja", d / "__init__.py", {})
    
    # Infrastructure layer
    infra_database = infrastructure_dir / "database"
    infra_external = infrastructure_dir / "external_services"
    infra_repositories = infrastructure_dir / "repositories"
    
    for d in [infra_database, infra_external, infra_repositories]:
        _ensure_dir(d)
        _render_and_write("service/app/__init__.py.jinja", d / "__init__.py", {})
    
    # Presentation layer
    pres_api = presentation_dir / "api"
    pres_controllers = presentation_dir / "controllers"
    pres_schemas = presentation_dir / "schemas"
    
    for d in [pres_api, pres_controllers, pres_schemas]:
        _ensure_dir(d)
        _render_and_write("service/app/__init__.py.jinja", d / "__init__.py", {})
    
    # Create API routes file
    _render_and_write("project/onion/presentation_routes.py.jinja", 
                     pres_api / "routes.py", {})
    
    # Create main application file
    _render_and_write("project/onion/main.py.jinja", src_root / "main.py", 
                     {"project_name": project_name})
    
    # Create dependency injection setup
    if config.get("include_di", True):
        _render_and_write("project/onion/container.py.jinja", src_root / "container.py", {})
    
    # Create tests directory with proper structure
    tests_root = base_path / "tests"
    tests_unit = tests_root / "unit"
    tests_integration = tests_root / "integration"
    
    for d in [tests_unit, tests_integration]:
        _ensure_dir(d)
        _render_and_write("service/app/__init__.py.jinja", d / "__init__.py", {})


def _scaffold_rest_api_service(service_path: Path, service_name: str, auth_type: AuthType, db_choice: DbType, cache_choice: CacheType) -> None:
    """Scaffold a REST API service using the new template structure."""
    src_app = service_path / "app"
    api_dir = src_app / "api"
    v1_dir = api_dir / "v1"
    core_dir = src_app / "core"
    models_dir = src_app / "models"
    services_dir = src_app / "services"
    repositories_dir = src_app / "repositories"
    middleware_dir = src_app / "middleware"
    schemas_dir = src_app / "schemas"
    utils_dir = src_app / "utils"
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
        middleware_dir,
        schemas_dir,
        utils_dir,
        tests_dir,
        infra_dir,
    ]:
        _ensure_dir(d)

    if auth_type != "none":
        _ensure_dir(auth_dir)
        _render_and_write("project/rest-apis/app/auth/__init__.py.jinja",
                          auth_dir / "__init__.py", {})
        _render_and_write("project/rest-apis/app/auth/routes.py.jinja",
                          auth_dir / "routes.py", {})

    if db_choice != "none":
        _ensure_dir(db_dir)
        _render_and_write("project/rest-apis/app/db/__init__.py.jinja",
                          db_dir / "__init__.py", {})
        _render_and_write("project/rest-apis/app/db/session.py.jinja",
                          db_dir / "session.py", {})

    if cache_choice != "none":
        _ensure_dir(cache_dir)
        _render_and_write("project/rest-apis/app/cache/__init__.py.jinja",
                          cache_dir / "__init__.py", {})
        _render_and_write("project/rest-apis/app/cache/client.py.jinja",
                          cache_dir / "client.py", {})

    _render_and_write("project/rest-apis/app/__init__.py.jinja",
                      src_app / "__init__.py", {})
    _render_and_write("project/rest-apis/app/main.py.jinja", src_app /
                      "main.py", {"title": service_name})
    _render_and_write("project/rest-apis/app/core/__init__.py.jinja",
                      core_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/app/core/config.py.jinja",
                      core_dir / "config.py", {})
    _render_and_write("project/rest-apis/app/api/__init__.py.jinja",
                      api_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/app/api/v1/__init__.py.jinja",
                      v1_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/app/api/v1/routes.py.jinja",
                      v1_dir / "routes.py", {})
    _render_and_write("project/rest-apis/app/models/__init__.py.jinja",
                      models_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/app/services/__init__.py.jinja",
                      services_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/app/repositories/__init__.py.jinja",
                      repositories_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/app/middleware/__init__.py.jinja",
                      middleware_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/app/middleware/error_handler.py.jinja",
                      middleware_dir / "error_handler.py", {})
    _render_and_write("project/rest-apis/app/schemas/__init__.py.jinja",
                      schemas_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/app/utils/__init__.py.jinja",
                      utils_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/app/utils/logger.py.jinja",
                      utils_dir / "logger.py", {})
    _render_and_write("project/rest-apis/tests/__init__.py.jinja",
                      tests_dir / "__init__.py", {})
    _render_and_write("project/rest-apis/infra/.gitkeep.jinja",
                      infra_dir / ".gitkeep", {})


def _scaffold_fullstack_backend(service_path: Path, service_name: str, auth_type: AuthType, db_choice: DbType, cache_choice: CacheType) -> None:
    """Scaffold a fullstack backend using fullstack-specific templates."""
    src_app = service_path / "app"
    api_dir = src_app / "api"
    v1_dir = api_dir / "v1"
    core_dir = src_app / "core"
    models_dir = src_app / "models"
    services_dir = src_app / "services"
    repositories_dir = src_app / "repositories"
    middleware_dir = src_app / "middleware"
    schemas_dir = src_app / "schemas"
    utils_dir = src_app / "utils"
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
        middleware_dir,
        schemas_dir,
        utils_dir,
        tests_dir,
        infra_dir,
    ]:
        _ensure_dir(d)

    if auth_type != "none":
        _ensure_dir(auth_dir)
        _render_and_write("project/fullstack/backend/app/auth/__init__.py.jinja",
                          auth_dir / "__init__.py", {})
        _render_and_write("project/fullstack/backend/app/auth/routes.py.jinja",
                          auth_dir / "routes.py", {})

    if db_choice != "none":
        _ensure_dir(db_dir)
        _render_and_write("project/fullstack/backend/app/db/__init__.py.jinja",
                          db_dir / "__init__.py", {})
        _render_and_write("project/fullstack/backend/app/db/session.py.jinja",
                          db_dir / "session.py", {})

    if cache_choice != "none":
        _ensure_dir(cache_dir)
        _render_and_write("project/fullstack/backend/app/cache/__init__.py.jinja",
                          cache_dir / "__init__.py", {})
        _render_and_write("project/fullstack/backend/app/cache/client.py.jinja",
                          cache_dir / "client.py", {})

    _render_and_write("project/fullstack/backend/app/__init__.py.jinja",
                      src_app / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/main.py.jinja", src_app /
                      "main.py", {"title": service_name})
    _render_and_write("project/fullstack/backend/app/core/__init__.py.jinja",
                      core_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/core/config.py.jinja",
                      core_dir / "config.py", {})
    _render_and_write("project/fullstack/backend/app/api/__init__.py.jinja",
                      api_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/api/v1/__init__.py.jinja",
                      v1_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/api/v1/routes.py.jinja",
                      v1_dir / "routes.py", {})
    _render_and_write("project/fullstack/backend/app/models/__init__.py.jinja",
                      models_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/services/__init__.py.jinja",
                      services_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/repositories/__init__.py.jinja",
                      repositories_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/middleware/__init__.py.jinja",
                      middleware_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/middleware/error_handler.py.jinja",
                      middleware_dir / "error_handler.py", {})
    _render_and_write("project/fullstack/backend/app/schemas/__init__.py.jinja",
                      schemas_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/utils/__init__.py.jinja",
                      utils_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/app/utils/logger.py.jinja",
                      utils_dir / "logger.py", {})
    _render_and_write("project/fullstack/backend/tests/__init__.py.jinja",
                      tests_dir / "__init__.py", {})
    _render_and_write("project/fullstack/backend/infra/.gitkeep.jinja",
                      infra_dir / ".gitkeep", {})


def _scaffold_service(service_path: Path, service_name: str, auth_type: AuthType, db_choice: DbType, cache_choice: CacheType) -> None:
    src_app = service_path / "app"
    api_dir = src_app / "api"
    v1_dir = api_dir / "v1"
    core_dir = src_app / "core"
    models_dir = src_app / "models"
    services_dir = src_app / "services"
    repositories_dir = src_app / "repositories"
    middleware_dir = src_app / "middleware"
    schemas_dir = src_app / "schemas"
    utils_dir = src_app / "utils"
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
        middleware_dir,
        schemas_dir,
        utils_dir,
        tests_dir,
        infra_dir,
    ]:
        _ensure_dir(d)

    if auth_type != "none":
        _ensure_dir(auth_dir)
        _render_and_write("service/app/auth/__init__.py.jinja",
                          auth_dir / "__init__.py", {})
        _render_and_write("service/app/auth/routes.py.jinja",
                          auth_dir / "routes.py", {})

    if db_choice != "none":
        _ensure_dir(db_dir)
        _render_and_write("service/app/db/__init__.py.jinja",
                          db_dir / "__init__.py", {})
        _render_and_write("service/app/db/session.py.jinja",
                          db_dir / "session.py", {})

    if cache_choice != "none":
        _ensure_dir(cache_dir)
        _render_and_write("service/app/cache/__init__.py.jinja",
                          cache_dir / "__init__.py", {})
        _render_and_write("service/app/cache/client.py.jinja",
                          cache_dir / "client.py", {})

    _render_and_write("service/app/__init__.py.jinja",
                      src_app / "__init__.py", {})
    _render_and_write("service/app/main.py.jinja", src_app /
                      "main.py", {"title": service_name})
    _render_and_write("service/app/core/__init__.py.jinja",
                      core_dir / "__init__.py", {})
    _render_and_write("service/app/core/config.py.jinja",
                      core_dir / "config.py", {})
    _render_and_write("service/app/api/__init__.py.jinja",
                      api_dir / "__init__.py", {})
    _render_and_write("service/app/api/v1/__init__.py.jinja",
                      v1_dir / "__init__.py", {})
    _render_and_write("service/app/api/v1/routes.py.jinja",
                      v1_dir / "routes.py", {})
    _render_and_write("service/app/models/__init__.py.jinja",
                      models_dir / "__init__.py", {})
    _render_and_write("service/app/services/__init__.py.jinja",
                      services_dir / "__init__.py", {})
    _render_and_write("service/app/repositories/__init__.py.jinja",
                      repositories_dir / "__init__.py", {})
    _render_and_write("service/app/middleware/__init__.py.jinja",
                      middleware_dir / "__init__.py", {})
    _render_and_write("service/app/middleware/error_handler.py.jinja",
                      middleware_dir / "error_handler.py", {})
    _render_and_write("service/app/schemas/__init__.py.jinja",
                      schemas_dir / "__init__.py", {})
    _render_and_write("service/app/utils/__init__.py.jinja",
                      utils_dir / "__init__.py", {})
    _render_and_write("service/app/utils/logger.py.jinja",
                      utils_dir / "logger.py", {})
    _render_and_write("service/tests/__init__.py.jinja",
                      tests_dir / "__init__.py", {})
    _render_and_write("service/infra/.gitkeep.jinja",
                      infra_dir / ".gitkeep", {})


def _scaffold_fullstack_frontend(
    frontend_root: Path,
    project_name: str,
    framework: FrontendFramework,
    build_tool: BuildTool,
    auth_type: AuthType,
    language: LanguageType = "typescript",
    backend_url: str = "http://localhost:8000"
) -> None:
    """Scaffold a complete frontend structure based on framework and build tool."""
    
    # Create base directories
    src_dir = frontend_root / "src"
    public_dir = frontend_root / "public"
    
    _ensure_dir(frontend_root)
    _ensure_dir(src_dir)
    _ensure_dir(public_dir)
    
    # Framework-specific context
    context = {
        "project_name": project_name,
        "framework": framework,
        "build_tool": build_tool,
        "auth_type": auth_type,
        "language": language,
        "backend_url": backend_url,
        "has_auth": auth_type != "none",
        "is_typescript": language == "typescript",
        "is_javascript": language == "javascript",
        "file_ext": "ts" if language == "typescript" else "js",
        "jsx_ext": "tsx" if language == "typescript" else "jsx"
    }
    
    if framework == "react":
        _scaffold_react_frontend(frontend_root, src_dir, public_dir, build_tool, language, context)
    elif framework == "angular":
        _scaffold_angular_frontend(frontend_root, src_dir, public_dir, language, context)
    elif framework == "vue":
        _scaffold_vue_frontend(frontend_root, src_dir, public_dir, build_tool, language, context)
    elif framework == "vanilla":
        _scaffold_vanilla_frontend(frontend_root, src_dir, public_dir, build_tool, language, context)
    
    # Common files for all frameworks
    _render_and_write(f"project/fullstack/frontend/{framework}/.gitignore.jinja",
                      frontend_root / ".gitignore", context)
    _render_and_write(f"project/fullstack/frontend/{framework}/README.md.jinja",
                      frontend_root / "README.md", context)


def _scaffold_react_frontend(frontend_root: Path, src_dir: Path, public_dir: Path, build_tool: BuildTool, language: LanguageType, context: dict) -> None:
    """Scaffold React frontend with complete structure."""
    
    # Create React-specific directories
    components_dir = src_dir / "components"
    pages_dir = src_dir / "pages"
    hooks_dir = src_dir / "hooks"
    services_dir = src_dir / "services"
    utils_dir = src_dir / "utils"
    styles_dir = src_dir / "styles"
    types_dir = src_dir / "types"
    
    for d in [components_dir, pages_dir, hooks_dir, services_dir, utils_dir, styles_dir, types_dir]:
        _ensure_dir(d)
    
    # Auth-specific directories if auth is enabled
    if context["has_auth"]:
        auth_dir = src_dir / "auth"
        _ensure_dir(auth_dir)
        
        # Auth components and services
        _render_and_write("project/fullstack/frontend/react/src/auth/AuthContext.tsx.jinja",
                          auth_dir / f"AuthContext.{context['jsx_ext']}", context)
        _render_and_write("project/fullstack/frontend/react/src/auth/AuthService.ts.jinja",
                          auth_dir / f"AuthService.{context['file_ext']}", context)
        _render_and_write("project/fullstack/frontend/react/src/auth/ProtectedRoute.tsx.jinja",
                          auth_dir / f"ProtectedRoute.{context['jsx_ext']}", context)
    
    # Core React files
    main_ext = context["jsx_ext"]
    app_ext = context["jsx_ext"]
    
    _render_and_write("project/fullstack/frontend/react/src/main.tsx.jinja",
                      src_dir / f"main.{main_ext}", context)
    _render_and_write("project/fullstack/frontend/react/src/App.tsx.jinja",
                      src_dir / f"App.{app_ext}", context)
    _render_and_write("project/fullstack/frontend/react/src/App.css.jinja",
                      src_dir / "App.css", context)
    
    # Components
    _render_and_write("project/fullstack/frontend/react/src/components/Header.tsx.jinja",
                      components_dir / f"Header.{context['jsx_ext']}", context)
    _render_and_write("project/fullstack/frontend/react/src/components/Layout.tsx.jinja",
                      components_dir / f"Layout.{context['jsx_ext']}", context)
    
    # Pages
    _render_and_write("project/fullstack/frontend/react/src/pages/Home.tsx.jinja",
                      pages_dir / f"Home.{context['jsx_ext']}", context)
    
    if context["has_auth"]:
        _render_and_write("project/fullstack/frontend/react/src/pages/Login.tsx.jinja",
                          pages_dir / f"Login.{context['jsx_ext']}", context)
        _render_and_write("project/fullstack/frontend/react/src/pages/Dashboard.tsx.jinja",
                          pages_dir / f"Dashboard.{context['jsx_ext']}", context)
    
    # Services
    _render_and_write("project/fullstack/frontend/react/src/services/api.ts.jinja",
                      services_dir / f"api.{context['file_ext']}", context)
    
    # Utils
    _render_and_write("project/fullstack/frontend/react/src/utils/constants.ts.jinja",
                      utils_dir / f"constants.{context['file_ext']}", context)
    
    # Types (only for TypeScript)
    if context["is_typescript"]:
        _render_and_write("project/fullstack/frontend/react/src/types/index.ts.jinja",
                          types_dir / "index.ts", context)
    
    # Styles
    _render_and_write("project/fullstack/frontend/react/src/styles/globals.css.jinja",
                      styles_dir / "globals.css", context)
    
    # Public files
    _render_and_write("project/fullstack/frontend/react/public/index.html.jinja",
                      public_dir / "index.html", context)
    
    # Build tool specific files
    if build_tool == "vite":
        if context["is_typescript"]:
            _render_and_write("project/fullstack/frontend/react/vite.config.ts.jinja",
                              frontend_root / "vite.config.ts", context)
        else:
            _render_and_write("project/fullstack/frontend/react/vite.config.js.jinja",
                              frontend_root / "vite.config.js", context)
        _render_and_write("project/fullstack/frontend/react/package-vite.json.jinja",
                          frontend_root / "package.json", context)
    elif build_tool == "create-react-app":
        _render_and_write("project/fullstack/frontend/react/package-cra.json.jinja",
                          frontend_root / "package.json", context)
    
    # TypeScript config (only for TypeScript projects)
    if context["is_typescript"]:
        _render_and_write("project/fullstack/frontend/react/tsconfig.json.jinja",
                          frontend_root / "tsconfig.json", context)
    
    # ESLint config (new flat config format)
    _render_and_write("project/fullstack/frontend/react/eslint.config.js.jinja",
                      frontend_root / "eslint.config.js", context)


def _scaffold_angular_frontend(frontend_root: Path, src_dir: Path, public_dir: Path, language: LanguageType, context: dict) -> None:
    """Scaffold Angular frontend with complete structure."""
    
    # Create Angular-specific directories
    app_dir = src_dir / "app"
    components_dir = app_dir / "components"
    pages_dir = app_dir / "pages"
    services_dir = app_dir / "services"
    guards_dir = app_dir / "guards"
    models_dir = app_dir / "models"
    
    for d in [app_dir, components_dir, pages_dir, services_dir, guards_dir, models_dir]:
        _ensure_dir(d)
    
    # Auth-specific setup if auth is enabled
    if context["has_auth"]:
        auth_dir = app_dir / "auth"
        _ensure_dir(auth_dir)
        
        # Auth services and guards
        _render_and_write("project/fullstack/frontend/angular/src/app/auth/auth.service.ts.jinja",
                          auth_dir / "auth.service.ts", context)
        _render_and_write("project/fullstack/frontend/angular/src/app/guards/auth.guard.ts.jinja",
                          guards_dir / "auth.guard.ts", context)
    
    # Core Angular files
    _render_and_write("project/fullstack/frontend/angular/src/main.ts.jinja",
                      src_dir / "main.ts", context)
    _render_and_write("project/fullstack/frontend/angular/src/app/app.component.ts.jinja",
                      app_dir / "app.component.ts", context)
    _render_and_write("project/fullstack/frontend/angular/src/app/app.component.html.jinja",
                      app_dir / "app.component.html", context)
    _render_and_write("project/fullstack/frontend/angular/src/app/app.component.css.jinja",
                      app_dir / "app.component.css", context)
    _render_and_write("project/fullstack/frontend/angular/src/app/app.module.ts.jinja",
                      app_dir / "app.module.ts", context)
    _render_and_write("project/fullstack/frontend/angular/src/app/app-routing.module.ts.jinja",
                      app_dir / "app-routing.module.ts", context)
    
    # Components
    _render_and_write("project/fullstack/frontend/angular/src/app/components/header.component.ts.jinja",
                      components_dir / "header.component.ts", context)
    
    # Pages
    _render_and_write("project/fullstack/frontend/angular/src/app/pages/home.component.ts.jinja",
                      pages_dir / "home.component.ts", context)
    
    if context["has_auth"]:
        _render_and_write("project/fullstack/frontend/angular/src/app/pages/login.component.ts.jinja",
                          pages_dir / "login.component.ts", context)
        _render_and_write("project/fullstack/frontend/angular/src/app/pages/dashboard.component.ts.jinja",
                          pages_dir / "dashboard.component.ts", context)
    
    # Services
    _render_and_write("project/fullstack/frontend/angular/src/app/services/api.service.ts.jinja",
                      services_dir / "api.service.ts", context)
    
    # Models
    _render_and_write("project/fullstack/frontend/angular/src/app/models/index.ts.jinja",
                      models_dir / "index.ts", context)
    
    # Angular config files
    _render_and_write("project/fullstack/frontend/angular/angular.json.jinja",
                      frontend_root / "angular.json", context)
    _render_and_write("project/fullstack/frontend/angular/package.json.jinja",
                      frontend_root / "package.json", context)
    _render_and_write("project/fullstack/frontend/angular/tsconfig.json.jinja",
                      frontend_root / "tsconfig.json", context)
    _render_and_write("project/fullstack/frontend/angular/tsconfig.app.json.jinja",
                      frontend_root / "tsconfig.app.json", context)


def _scaffold_vue_frontend(frontend_root: Path, src_dir: Path, public_dir: Path, build_tool: BuildTool, language: LanguageType, context: dict) -> None:
    """Scaffold Vue frontend with complete structure."""
    
    # Create Vue-specific directories
    components_dir = src_dir / "components"
    views_dir = src_dir / "views"
    router_dir = src_dir / "router"
    store_dir = src_dir / "store"
    services_dir = src_dir / "services"
    utils_dir = src_dir / "utils"
    
    for d in [components_dir, views_dir, router_dir, store_dir, services_dir, utils_dir]:
        _ensure_dir(d)
    
    # Auth-specific setup if auth is enabled
    if context["has_auth"]:
        auth_dir = src_dir / "auth"
        _ensure_dir(auth_dir)
        
        _render_and_write("project/fullstack/frontend/vue/src/auth/authService.ts.jinja",
                          auth_dir / "authService.ts", context)
        _render_and_write("project/fullstack/frontend/vue/src/store/auth.ts.jinja",
                          store_dir / "auth.ts", context)
    
    # Core Vue files
    _render_and_write("project/fullstack/frontend/vue/src/main.ts.jinja",
                      src_dir / "main.ts", context)
    _render_and_write("project/fullstack/frontend/vue/src/App.vue.jinja",
                      src_dir / "App.vue", context)
    
    # Router
    _render_and_write("project/fullstack/frontend/vue/src/router/index.ts.jinja",
                      router_dir / "index.ts", context)
    
    # Store
    _render_and_write("project/fullstack/frontend/vue/src/store/index.ts.jinja",
                      store_dir / "index.ts", context)
    
    # Components
    _render_and_write("project/fullstack/frontend/vue/src/components/Header.vue.jinja",
                      components_dir / "Header.vue", context)
    
    # Views
    _render_and_write("project/fullstack/frontend/vue/src/views/Home.vue.jinja",
                      views_dir / "Home.vue", context)
    
    if context["has_auth"]:
        _render_and_write("project/fullstack/frontend/vue/src/views/Login.vue.jinja",
                          views_dir / "Login.vue", context)
        _render_and_write("project/fullstack/frontend/vue/src/views/Dashboard.vue.jinja",
                          views_dir / "Dashboard.vue", context)
    
    # Services
    _render_and_write("project/fullstack/frontend/vue/src/services/api.ts.jinja",
                      services_dir / "api.ts", context)
    
    # Public files
    _render_and_write("project/fullstack/frontend/vue/public/index.html.jinja",
                      public_dir / "index.html", context)
    
    # Build tool specific files
    if build_tool == "vite":
        _render_and_write("project/fullstack/frontend/vue/vite.config.ts.jinja",
                          frontend_root / "vite.config.ts", context)
        _render_and_write("project/fullstack/frontend/vue/package-vite.json.jinja",
                          frontend_root / "package.json", context)
    
    # TypeScript config
    _render_and_write("project/fullstack/frontend/vue/tsconfig.json.jinja",
                      frontend_root / "tsconfig.json", context)


def _scaffold_vanilla_frontend(frontend_root: Path, src_dir: Path, public_dir: Path, build_tool: BuildTool, language: LanguageType, context: dict) -> None:
    """Scaffold Vanilla JS/TS frontend with complete structure."""
    
    # Create directories
    js_dir = src_dir / "js"
    css_dir = src_dir / "css"
    assets_dir = src_dir / "assets"
    
    for d in [js_dir, css_dir, assets_dir]:
        _ensure_dir(d)
    
    # Auth-specific setup if auth is enabled
    if context["has_auth"]:
        auth_dir = js_dir / "auth"
        _ensure_dir(auth_dir)
        
        _render_and_write("project/fullstack/frontend/vanilla/src/js/auth/authService.ts.jinja",
                          auth_dir / "authService.ts", context)
    
    # Core files
    _render_and_write("project/fullstack/frontend/vanilla/src/js/main.ts.jinja",
                      js_dir / "main.ts", context)
    _render_and_write("project/fullstack/frontend/vanilla/src/js/api.ts.jinja",
                      js_dir / "api.ts", context)
    
    # CSS
    _render_and_write("project/fullstack/frontend/vanilla/src/css/styles.css.jinja",
                      css_dir / "styles.css", context)
    
    # HTML
    _render_and_write("project/fullstack/frontend/vanilla/public/index.html.jinja",
                      public_dir / "index.html", context)
    
    # Build tool specific files
    if build_tool == "vite":
        _render_and_write("project/fullstack/frontend/vanilla/vite.config.ts.jinja",
                          frontend_root / "vite.config.ts", context)
        _render_and_write("project/fullstack/frontend/vanilla/package-vite.json.jinja",
                          frontend_root / "package.json", context)
    elif build_tool == "webpack":
        _render_and_write("project/fullstack/frontend/vanilla/webpack.config.js.jinja",
                          frontend_root / "webpack.config.js", context)
        _render_and_write("project/fullstack/frontend/vanilla/package-webpack.json.jinja",
                          frontend_root / "package.json", context)
    
    # TypeScript config
    _render_and_write("project/fullstack/frontend/vanilla/tsconfig.json.jinja",
                      frontend_root / "tsconfig.json", context)


def scaffold_project_structure(
    *,
    base_path: Path,
    project_name: str,
    architecture: ArchitectureType = "rest-apis",
    auth_type: AuthType = "none",
    db_choice: DbType = "none",
    cache_choice: CacheType = "none",
    architecture_config: dict = None,
    frontend_config: dict = None,
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
        _scaffold_rest_api_service(app_root, project_name, auth_type,
                                 db_choice, cache_choice)

    elif architecture == "fullstack":
        # Handle Fullstack architecture
        # Backend part (using fullstack-specific templates)
        backend_root = app_root / "backend"
        _scaffold_fullstack_backend(backend_root, project_name,
                          auth_type, db_choice, cache_choice)

        # Frontend part - comprehensive scaffolding
        frontend_root = app_root / "frontend"
        
        if frontend_config:
            framework = frontend_config.get("framework", "react")
            build_tool = frontend_config.get("build_tool", "vite")
            language = frontend_config.get("language", "typescript")
            
            # Use the comprehensive frontend scaffolding
            _scaffold_fullstack_frontend(
                frontend_root=frontend_root,
                project_name=project_name,
                framework=framework,
                build_tool=build_tool,
                auth_type=auth_type,
                language=language,
                backend_url="http://localhost:8000"
            )
        else:
            # Default fallback - React with Vite and TypeScript
            _scaffold_fullstack_frontend(
                frontend_root=frontend_root,
                project_name=project_name,
                framework="react",
                build_tool="vite",
                auth_type=auth_type,
                language="typescript",
                backend_url="http://localhost:8000"
            )

    elif architecture == "microservices":
        # Handle Microservices architecture
        _scaffold_microservices(app_root, project_name, auth_type, 
                               db_choice, cache_choice, architecture_config or {})

    elif architecture == "onion-architecture":
        # Handle Onion architecture
        _scaffold_onion_architecture(app_root, project_name, auth_type,
                                    db_choice, cache_choice, architecture_config or {})

    # UV/pyproject setup and top-level files
    _render_and_write("project/pyproject.toml.jinja", app_root /
                      "pyproject.toml", {"project_name": project_name})
    _render_and_write("project/README.md.jinja", app_root /
                      "README.md", {"project_name": project_name, "architecture": architecture})
    _render_and_write("project/.gitignore.jinja", app_root / ".gitignore", {})
