"""Add service command for adding new services to existing projects."""

import os
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console

from fastkit.shared.ui import print_ascii_msg, show_loading_animation
from fastkit.shared.service_help import display_service_help, create_service_overview_table, create_service_examples_panel
from fastkit.generators.service_generator import add_service_to_project
from rich.columns import Columns

console = Console()


def add_service(
    service_type: Optional[str] = typer.Argument(
        None,
        help="🔧 Service type: db | cache | auth | jobs",
        metavar="SERVICE_TYPE"
    ),
    service_provider: Optional[str] = typer.Argument(
        None,
        help="⚙️  Provider: postgresql|mysql|sqlite|mongodb|mssql|redis|memcached|dynamodb|in-memory|jwt|oauth|celery|rq|apscheduler|dramatiq|arq",
        metavar="PROVIDER"
    ),
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="📁 Path to the project root (default: current directory)",
        metavar="PATH"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="🔄 Overwrite existing service if it exists"
    ),
    help_flag: bool = typer.Option(
        False,
        "--help",
        "-h",
        help="Show comprehensive service guide",
        is_eager=True
    )
):
    """
    🔧 Add a production-ready service to your FastAPI project.

    This command integrates services with proper configuration, dependencies,
    and best practices. Each service includes client setup, configuration
    management, and integration patterns.

    🎯 AVAILABLE SERVICES:
        • Database (db)    - PostgreSQL, MySQL, SQLite, MongoDB, SQL Server
        • Cache (cache)    - Redis, Memcached, DynamoDB, In-Memory
        • Auth (auth)      - JWT tokens, OAuth 2.0
        • Jobs (jobs)      - Celery, RQ, APScheduler, Dramatiq, ARQ

    📋 QUICK EXAMPLES:
        fastkit add-service db postgresql     # Production database
        fastkit add-service cache redis       # High-performance cache
        fastkit add-service auth jwt          # Token authentication
        fastkit add-service jobs celery       # Background tasks

    💡 TIP: Run 'fastkit add-service --help' to see the full service guide
         with detailed comparisons and recommendations.
    """
    # Handle custom help display or missing arguments
    if help_flag or service_type is None or service_provider is None:
        display_service_help()
        raise typer.Exit()
    
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
            f"[bold red]❌ Error:[/bold red] Invalid service combination '{service_type}' with '{service_provider}'.\n")
        
        # Show beautiful service help
        console.print("[bold bright_cyan]📖 Available Services Guide:[/bold bright_cyan]\n")
        
        # Display service overview tables
        service_panels = create_service_overview_table()
        
        # Display in 2x2 grid
        top_row = Columns([service_panels[0], service_panels[1]], equal=True, expand=True)
        bottom_row = Columns([service_panels[2], service_panels[3]], equal=True, expand=True)
        
        console.print(top_row)
        console.print()
        console.print(bottom_row)
        console.print()
        
        # Show examples
        examples_panel = create_service_examples_panel()
        console.print(examples_panel)
        console.print()
        
        console.print(
            "[dim]💡 Use 'fastkit add-service --help' for the complete service guide.[/dim]")
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
