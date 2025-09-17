import os
import typer
from pathlib import Path
from typing import Optional
from InquirerPy import inquirer
from rich.console import Console

from fastkit.shared.ui import print_ascii_msg, show_loading_animation
from fastkit.generators.project_generator import scaffold_project_structure


console = Console()


def _prompt_with_choices(prompt_text: str, choices: list[str], default: str | None = None) -> str:
    """
    Prompt the user to select from a list of choices using an interactive menu
    (arrow keys + enter).
    """
    value = inquirer.select(
        message=prompt_text,
        choices=choices,
        default=default or choices[0],
        pointer="👉",
        qmark="❓",
    ).execute()

    return value.lower()


def _normalize_db_choice(db_choice: str) -> str:
    mapping = {
        "postgres": "postgresql",
        "postgresql": "postgresql",
        "psql": "postgresql",
        "sqlite": "sqlite",
        "mysql": "mysql",
        "mssql": "mssql",
        "sqlserver": "mssql",
        "mongodb": "mongodb",
        "mongo": "mongodb",
        "none": "none",
    }
    return mapping.get(db_choice.lower(), db_choice.lower())


def _normalize_cache_choice(cache_choice: str) -> str:
    mapping = {
        "redis": "redis",
        "none": "none",
    }
    return mapping.get(cache_choice.lower(), cache_choice.lower())


def _normalize_architecture_choice(architecture: str) -> str:
    mapping = {
        "fullstack application": "fullstack",
        "microservices architecture": "microservices",
        "rest api service": "rest-apis",
        "onion architecture": "onion-architecture",
    }
    return mapping.get(architecture.lower(), architecture.lower())


def _get_microservices_config() -> dict:
    """Get microservices-specific configuration from user."""
    console.print("\n[bold]Microservices Configuration[/bold]")
    
    # Ask for number of services
    num_services = typer.prompt(
        "How many services do you want to create?", 
        type=int, 
        default=2
    )
    
    services = []
    console.print(f"\nEnter names for {num_services} services:")
    
    for i in range(num_services):
        service_name = typer.prompt(
            f"Service {i+1} name", 
            default=f"service-{i+1}"
        ).strip().lower().replace(" ", "-")
        services.append(service_name)
    
    # Ask about API Gateway
    include_gateway = typer.confirm(
        "Include API Gateway service?", 
        default=True
    )
    
    return {
        "services": services,
        "include_gateway": include_gateway,
        "include_shared": True  # Always include shared libraries
    }


def _get_onion_architecture_config() -> dict:
    """Get onion architecture-specific configuration from user."""
    console.print("\n[bold]Onion Architecture Configuration[/bold]")
    
    # Ask about domain complexity
    domain_entities = typer.prompt(
        "Enter main domain entities (comma-separated)", 
        default="User,Product"
    ).strip()
    
    entities = [entity.strip() for entity in domain_entities.split(",") if entity.strip()]
    
    # Ask about use cases
    include_cqrs = typer.confirm(
        "Include CQRS pattern (Command/Query separation)?", 
        default=False
    )
    
    return {
        "entities": entities,
        "include_cqrs": include_cqrs,
        "include_di": True  # Always include dependency injection
    }


def create_project(
    project_name: Optional[str] = typer.Argument(
        None, help="Name of the project to create (e.g., myapp)"
    ),
    path: Optional[Path] = typer.Option(
        None, "--path", "-p", help="Directory to create the project in"
    ),
):
    """Create a new FastAPI project via an interactive wizard (structure only)."""
    console.clear()
    print_ascii_msg()

    console.print(
        "[bold bright_cyan]Let's set up your FastAPI project structure[/bold bright_cyan]\n")

    if not project_name:
        project_name = typer.prompt(
            "Project name", default="my-fastapi-app").strip()
    else:
        project_name = project_name.strip()

    if path is None:
        target_dir_input = typer.prompt(
            "Target directory (absolute or relative)", default=os.getcwd()).strip()
        base_path = Path(target_dir_input).expanduser().resolve()
    else:
        base_path = Path(path).expanduser().resolve()

    target_dir = base_path / project_name

    if target_dir.exists() and any(target_dir.iterdir()):
        overwrite = typer.confirm(
            f"Directory '{target_dir}' already exists and is not empty. Continue?", default=False)
        if not overwrite:
            typer.echo("Aborting.")
            raise typer.Exit(code=1)

    architecture = _normalize_architecture_choice(
        _prompt_with_choices(
            "Select project architecture",
            [
                "Fullstack Application",
                "Microservices Architecture",
                "REST API Service",
                "Onion Architecture"
            ],
            default="REST API Service",
        )
    )

    frontend_config = {}
    if architecture == "fullstack":
        console.print("\n[bold]Frontend Configuration[/bold]")
        
        frontend_framework = _prompt_with_choices(
            "Select frontend framework",
            ["React", "Angular", "Vue", "Vanilla"],
            default="React",
        )
        
        # Build tool selection based on framework
        if frontend_framework.lower() == "react":
            build_tool = _prompt_with_choices(
                "Select build tool for React",
                ["Vite", "Create React App"],
                default="Vite",
            )
            # Normalize build tool name
            build_tool = "create-react-app" if build_tool.lower() == "create react app" else build_tool.lower()
        elif frontend_framework.lower() == "angular":
            build_tool = "angular-cli"  # Angular uses CLI by default
        elif frontend_framework.lower() == "vue":
            build_tool = _prompt_with_choices(
                "Select build tool for Vue",
                ["Vite", "Webpack"],
                default="Vite",
            ).lower()
        else:  # Vanilla
            build_tool = _prompt_with_choices(
                "Select build tool for Vanilla JS/TS",
                ["Vite", "Webpack"],
                default="Vite",
            ).lower()
        
        # Language selection
        language = _prompt_with_choices(
            "Select language",
            ["TypeScript", "JavaScript"],
            default="TypeScript",
        ).lower()
        
        frontend_config = {
            "framework": frontend_framework.lower(),
            "build_tool": build_tool,
            "language": language,
        }

    needs_auth = typer.confirm(
        "Do you want to include authentication setup?", default=False)
    auth_type = "none"
    if needs_auth:
        auth_type = _prompt_with_choices("Choose authentication type", [
                                         "jwt", "oauth"], default="jwt")

    needs_integrations = typer.confirm(
        "Do you need any external services (DB, cache)?", default=False)

    db_choice = "none"
    if needs_integrations and typer.confirm("Add a database integration?", default=False):
        db_choice = _normalize_db_choice(
            _prompt_with_choices(
                "Choose a database",
                ["postgresql", "sqlite", "mysql", "mongodb", "none"],
                default="sqlite",
            )
        )

    cache_choice = "none"
    if needs_integrations and typer.confirm("Add a caching system?", default=False):
        cache_choice = _normalize_cache_choice(
            _prompt_with_choices("Choose a cache provider", [
                                 "redis", "none"], default="redis")
        )

    # Get architecture-specific configuration
    architecture_config = {}
    if architecture == "microservices":
        architecture_config = _get_microservices_config()
    elif architecture == "onion_architecture":
        architecture_config = _get_onion_architecture_config()

    console.print()
    console.print("[bold]Summary[/bold]")
    console.print(f"  Project: [cyan]{project_name}[/cyan]")
    console.print(f"  Architecture: [cyan]{architecture}[/cyan]")
    if architecture == "fullstack":
        console.print(f"  Frontend: [cyan]{frontend_config['framework']} ({frontend_config['build_tool']}) - {frontend_config['language']}[/cyan]")
    console.print(f"  Auth:    [cyan]{auth_type}[/cyan]")
    console.print(f"  DB:      [cyan]{db_choice}[/cyan]")
    console.print(f"  Cache:   [cyan]{cache_choice}[/cyan]")
    
    if architecture_config:
        console.print(f"  Config:  [cyan]{architecture_config}[/cyan]")
    
    console.print()

    proceed = typer.confirm(
        "Proceed to create the directory structure?", default=True)
    if not proceed:
        typer.echo("Aborting.")
        raise typer.Exit(code=1)

    show_loading_animation()

    scaffold_project_structure(
        base_path=target_dir,
        project_name=project_name,
        architecture=architecture,
        auth_type=auth_type,
        db_choice=db_choice,
        cache_choice=cache_choice,
        architecture_config=architecture_config,
        frontend_config=frontend_config,
    )

    console.print(
        f"\n[bold bright_green]Project structure created at[/bold bright_green] [underline]{target_dir}[/underline]")

