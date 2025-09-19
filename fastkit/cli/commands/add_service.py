"""Add service command for adding new services to existing projects."""

import os
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console

from fastkit.shared.ui import print_ascii_msg, show_loading_animation
from fastkit.generators.service_generator import add_service_to_project

console = Console()


def add_service(
    service_type: str = typer.Argument(
        ..., help="Service type: 'db' (database), 'cache' (caching), 'auth' (authentication), 'jobs' (background jobs)"
    ),
    service_provider: str = typer.Argument(
        ..., help="Provider: DB(postgresql|mysql|sqlite|mongodb|mssql) CACHE(redis|memcached|dynamodb|in-memory) AUTH(jwt|oauth) JOBS(celery|rq|apscheduler|dramatiq|arq)"
    ),
    path: Optional[Path] = typer.Option(
        None, "--path", "-p", help="Path to the project root (defaults to current directory)"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing service if it exists"
    )
):
    """Add a new service to an existing FastAPI project.
    
    SERVICE TYPES:
      db      Database services with ORM/ODM support
      cache   Caching services for performance optimization  
      auth    Authentication and authorization services
      jobs    Background job scheduling and processing
    
    DATABASE PROVIDERS:
      postgresql  PostgreSQL with SQLAlchemy (production-ready)
      mysql       MySQL with SQLAlchemy (widely supported)
      sqlite      SQLite with SQLAlchemy (development/testing)
      mongodb     MongoDB with Motor (NoSQL document store)
      mssql       Microsoft SQL Server with SQLAlchemy
    
    CACHE PROVIDERS:
      redis       Redis in-memory cache (high performance)
      memcached   Memcached distributed cache (simple & fast)
      dynamodb    AWS DynamoDB cache (cloud-native)
      in-memory   Local memory cache (development/testing)
    
    AUTH PROVIDERS:
      jwt         JSON Web Token authentication
      oauth       OAuth 2.0 authentication (Google, GitHub, etc.)
    
    JOB PROVIDERS:
      celery      Celery distributed task queue (production-ready)
      rq          Redis Queue simple job processing (lightweight)
      apscheduler Advanced Python Scheduler (in-process)
      dramatiq    Modern alternative to Celery (simple & reliable)
      arq         Async Redis Queue (FastAPI-friendly)
    
    EXAMPLES:
      fastkit add-service db postgresql
      fastkit add-service cache redis
      fastkit add-service auth jwt
      fastkit add-service jobs celery
    """
    console.clear()
    print_ascii_msg()

    console.print(
        f"[bold bright_cyan]Adding {service_type} service ({service_provider}) to your project[/bold bright_cyan]\n")

    # Determine project path
    if path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(path).expanduser().resolve()

    # Validate project structure
    if not _is_valid_fastkit_project(project_path):
        console.print(
            "[bold red]Error:[/bold red] This doesn't appear to be a valid FastKit project.")
        console.print(
            "Make sure you're in a project created with 'fastkit create-project'.")
        raise typer.Exit(code=1)

    # Validate service type and provider
    if not _is_valid_service_combination(service_type, service_provider):
        console.print(
            f"[bold red]Error:[/bold red] Invalid service combination '{service_type}' with '{service_provider}'.")
        console.print("\n[bold]Available service combinations:[/bold]")
        
        console.print("\n[bold cyan]DATABASE SERVICES:[/bold cyan]")
        console.print("  [green]fastkit add-service db postgresql[/green]  # PostgreSQL with SQLAlchemy")
        console.print("  [green]fastkit add-service db mysql[/green]       # MySQL with SQLAlchemy")
        console.print("  [green]fastkit add-service db sqlite[/green]      # SQLite with SQLAlchemy")
        console.print("  [green]fastkit add-service db mongodb[/green]     # MongoDB with Motor")
        console.print("  [green]fastkit add-service db mssql[/green]       # Microsoft SQL Server")
        
        console.print("\n[bold cyan]CACHE SERVICES:[/bold cyan]")
        console.print("  [green]fastkit add-service cache redis[/green]       # Redis in-memory cache")
        console.print("  [green]fastkit add-service cache memcached[/green]   # Memcached distributed cache")
        console.print("  [green]fastkit add-service cache dynamodb[/green]    # AWS DynamoDB cache")
        console.print("  [green]fastkit add-service cache in-memory[/green]   # Local memory cache")
        
        console.print("\n[bold cyan]AUTH SERVICES:[/bold cyan]")
        console.print("  [green]fastkit add-service auth jwt[/green]    # JSON Web Token authentication")
        console.print("  [green]fastkit add-service auth oauth[/green]  # OAuth 2.0 authentication")
        
        console.print("\n[bold cyan]JOB SERVICES:[/bold cyan]")
        console.print("  [green]fastkit add-service jobs celery[/green]      # Celery distributed task queue")
        console.print("  [green]fastkit add-service jobs rq[/green]          # Redis Queue simple processing")
        console.print("  [green]fastkit add-service jobs apscheduler[/green] # Advanced Python Scheduler")
        console.print("  [green]fastkit add-service jobs dramatiq[/green]    # Modern Celery alternative")
        console.print("  [green]fastkit add-service jobs arq[/green]         # Async Redis Queue")
        
        console.print("\n[dim]Use --help for more detailed information about each service type.[/dim]")
        raise typer.Exit(code=1)

    # Check if service already exists
    if _service_exists(project_path, service_type) and not force:
        console.print(
            f"[bold yellow]Warning:[/bold yellow] {service_type.title()} service already exists.")
        overwrite = typer.confirm(
            "Do you want to overwrite it?", default=False)
        if not overwrite:
            console.print("Aborting.")
            raise typer.Exit(code=1)

    # Show summary
    console.print("[bold]Summary[/bold]")
    console.print(f"  Service Type: [cyan]{service_type}[/cyan]")
    console.print(f"  Provider:     [cyan]{service_provider}[/cyan]")
    console.print(f"  Project:      [cyan]{project_path}[/cyan]")
    console.print()

    proceed = typer.confirm("Proceed to add the service?", default=True)
    if not proceed:
        console.print("Aborting.")
        raise typer.Exit(code=1)

    show_loading_animation(
        f"Adding {service_type} service ({service_provider})...")

    # Add the service
    try:
        add_service_to_project(
            project_path=project_path,
            service_type=service_type,
            service_provider=service_provider,
            force=force
        )

        console.print(
            f"\n[bold bright_green]{service_type.title()} service ({service_provider}) added successfully![/bold bright_green]")
        console.print(
            "[dim]✓ Service files created[/dim]")
        console.print(
            "[dim]✓ Configuration updated[/dim]")
        console.print(
            "[dim]✓ Dependencies synced to pyproject.toml[/dim]")

        # Provide next steps based on service type
        _show_next_steps(service_type, service_provider)

    except Exception as e:
        console.print(
            f"\n[bold red]Error adding service:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


def _is_valid_fastkit_project(project_path: Path) -> bool:
    """Check if the current directory is a valid FastKit project."""
    required_paths = [
        project_path / "app",
        project_path / "app" / "core",
        project_path / "app" / "main.py",
        project_path / "pyproject.toml"
    ]

    return all(path.exists() for path in required_paths)


def _is_valid_service_combination(service_type: str, service_provider: str) -> bool:
    """Validate service type and provider combination."""
    valid_combinations = {
        "db": ["postgresql", "mysql", "sqlite", "mongodb", "mssql"],
        "cache": ["redis", "memcached", "dynamodb", "in-memory"],
        "auth": ["jwt", "oauth"],
        "jobs": ["celery", "rq", "apscheduler", "dramatiq", "arq"]
    }

    return service_type in valid_combinations and service_provider in valid_combinations[service_type]


def _service_exists(project_path: Path, service_type: str) -> bool:
    """Check if a service already exists."""
    service_paths = {
        "db": project_path / "app" / "db",
        "cache": project_path / "app" / "cache",
        "auth": project_path / "app" / "auth",
        "jobs": project_path / "app" / "jobs"
    }

    service_path = service_paths.get(service_type)
    return service_path and service_path.exists()


def _show_next_steps(service_type: str, service_provider: str):
    """Show next steps after adding a service."""
    console.print("\n[bold]Next steps:[/bold]")

    if service_type == "db":
        console.print(
            f"1. Update your environment variables for {service_provider} connection")
        console.print(
            "2. Create your database models in [cyan]app/models/[/cyan]")
        console.print("3. Run database migrations if needed")
        console.print(
            "4. Update [cyan]app/core/dependencies.py[/cyan] to include database dependency")

    elif service_type == "cache":
        console.print(
            f"1. Update your environment variables for {service_provider} connection")
        console.print(
            "2. Use the cache client in your services: [cyan]from app.cache import cache_client[/cyan]")
        console.print(
            "3. Update Docker Compose if using containerized development")

    elif service_type == "auth":
        console.print(
            f"1. Update your environment variables for {service_provider} configuration")
        console.print("2. Create user models and authentication endpoints")
        console.print(
            "3. Update [cyan]app/core/dependencies.py[/cyan] to include auth dependencies")
        console.print("4. Protect your routes with authentication decorators")

    elif service_type == "jobs":
        console.print(
            f"1. Review example tasks in [cyan]app/jobs/tasks.py[/cyan]")
        console.print(
            "2. Create your own tasks using the @task decorator")
        console.print(
            "3. Configure job schedules (cron, interval, one-time)")
        
        if service_provider in ["celery", "rq", "dramatiq", "arq"]:
            console.print(
                "4. Start Redis server for job queue backend")
            console.print(
                f"5. Start {service_provider} worker to process jobs")
        elif service_provider == "apscheduler":
            console.print(
                "4. Call scheduler.start() in your application startup")
        
        console.print(
            "6. Monitor job execution and handle failures")

    console.print("\n7. Restart your application to apply changes")
