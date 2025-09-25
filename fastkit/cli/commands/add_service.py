"""Add service command for adding new services to existing projects."""

import os
import typer
from pathlib import Path
from typing import Optional
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from fastkit.shared.ui import print_ascii_msg, show_loading_animation
from fastkit.shared.service_help import display_service_help, create_service_overview_table, create_service_examples_panel
from fastkit.generators.service_generator import add_service_to_project
from rich.columns import Columns

console = Console()


def _get_service_choices():
    """Get available service choices with descriptions."""
    return [
        Choice(
            value="db",
            name="🗄️  Database (db) - PostgreSQL, MySQL, SQLite, MongoDB, SQL Server"
        ),
        Choice(
            value="cache",
            name="⚡ Cache (cache) - Redis, Memcached, In-Memory"
        ),
        Choice(
            value="auth",
            name="🔐 Authentication (auth) - JWT tokens, OAuth 2.0"
        ),
        Choice(
            value="jobs",
            name="⚙️  Background Jobs (jobs) - Celery, RQ, APScheduler, Dramatiq, ARQ"
        )
    ]


def _get_provider_choices(service_type: str):
    """Get provider choices based on service type."""
    provider_choices = {
        "db": [
            Choice(
                value="postgresql",
                name="🐘 PostgreSQL - Production apps, complex queries, ACID compliance"
            ),
            Choice(
                value="mysql",
                name="🐬 MySQL - Web apps, high compatibility, proven reliability"
            ),
            Choice(
                value="sqlite",
                name="🗃️  SQLite - Development, small apps, embedded database"
            ),
            Choice(
                value="mongodb",
                name="🍃 MongoDB - Document storage, flexibility, NoSQL"
            ),
            Choice(
                value="mssql",
                name="🏢 SQL Server - Enterprise, Windows environments, Microsoft stack"
            )
        ],
        "cache": [
            Choice(
                value="redis",
                name="🔴 Redis - High performance, pub/sub, data structures"
            ),
            Choice(
                value="memcached",
                name="💾 Memcached - Simple caching, distributed, lightweight"
            ),
            Choice(
                value="in-memory",
                name="🧠 In-Memory - Development, testing, local cache"
            )
        ],
        "auth": [
            Choice(
                value="jwt",
                name="🎫 JWT - Token-based, stateless, APIs, microservices"
            ),
            Choice(
                value="oauth",
                name="🔗 OAuth 2.0 - Social login, third-party integration"
            )
        ],
        "jobs": [
            Choice(
                value="celery",
                name="🌿 Celery - Production, complex workflows, distributed"
            ),
            Choice(
                value="rq",
                name="📋 RQ - Simple, lightweight, Redis-based queue"
            ),
            Choice(
                value="dramatiq",
                name="🎭 Dramatiq - Modern, reliable, actor-based"
            ),
            Choice(
                value="arq",
                name="⚡ ARQ - FastAPI-friendly, async/await, Redis"
            ),
            Choice(
                value="apscheduler",
                name="⏰ APScheduler - Cron-like, in-process, scheduling"
            )
        ]
    }
    return provider_choices.get(service_type, [])


def _interactive_service_selection():
    """Interactive service and provider selection."""
    # Welcome message with consistent styling
    welcome_text = Text()
    welcome_text.append("🔧 Interactive Service Setup", style="bold bright_cyan")
    console.print(Align.center(welcome_text))
    console.print(Align.center("[dim]Let's help you choose the right service for your project[/dim]"))
    console.print()
    
    # Service selection info panel
    selection_info = Panel(
        "🎯 [bold]Service Selection Process:[/bold]\n"
        "• [cyan]Step 1[/cyan] - Choose service type (db, cache, auth, jobs)\n"
        "• [cyan]Step 2[/cyan] - Select provider based on your needs\n"
        "• [cyan]Step 3[/cyan] - Configure and integrate with your project\n\n"
        "💡 [bold]Each service includes:[/bold]\n"
        "• Production-ready configuration\n"
        "• Best practices implementation\n"
        "• Automatic dependency management",
        title="[bold bright_green]✨ Service Integration[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )
    console.print(selection_info)
    console.print()
    
    # Step 1: Choose service type
    console.print("[bold bright_cyan]Step 1: Choose Service Type[/bold bright_cyan]")
    service_type = inquirer.select(
        message="What type of service would you like to add?",
        choices=_get_service_choices(),
        default="db",
        pointer="👉"
    ).execute()
    
    # Show selection confirmation
    selection_text = Text()
    selection_text.append("✅ Selected service: ", style="bright_white")
    selection_text.append(f"{service_type}", style="bold bright_cyan")
    console.print(f"\n{selection_text}")
    console.print()
    
    # Step 2: Choose provider based on service type
    provider_choices = _get_provider_choices(service_type)
    
    console.print(f"[bold bright_cyan]Step 2: Choose {service_type.title()} Provider[/bold bright_cyan]")
    
    service_provider = inquirer.select(
        message=f"Which {service_type} provider would you like to use?",
        choices=provider_choices,
        default=provider_choices[0].value if provider_choices else None,
        pointer="👉"
    ).execute()
    
    # Show final selection
    provider_text = Text()
    provider_text.append("✅ Selected provider: ", style="bright_white")
    provider_text.append(f"{service_provider}", style="bold bright_cyan")
    console.print(f"\n{provider_text}")
    console.print()
    
    return service_type, service_provider


def _get_service_info_panel(service_type: str, service_provider: str):
    """Create service information panel."""
    service_descriptions = {
        "db": {
            "title": "🗄️  Database Service",
            "description": "Persistent data storage with ORM integration",
            "features": [
                "SQLAlchemy/Motor ORM setup",
                "Connection pooling & management",
                "Migration support",
                "Environment-based configuration"
            ]
        },
        "cache": {
            "title": "⚡ Cache Service",
            "description": "High-performance caching layer",
            "features": [
                "Async client configuration",
                "Serialization handling",
                "TTL and eviction policies",
                "Connection retry logic"
            ]
        },
        "auth": {
            "title": "🔐 Authentication Service",
            "description": "Secure user authentication & authorization",
            "features": [
                "Token generation & validation",
                "Password hashing utilities",
                "Middleware integration",
                "Role-based access control"
            ]
        },
        "jobs": {
            "title": "⚙️  Background Jobs Service",
            "description": "Asynchronous task processing",
            "features": [
                "Task queue management",
                "Scheduled job support",
                "Error handling & retries",
                "Monitoring & logging"
            ]
        }
    }
    
    provider_descriptions = {
        "postgresql": "Production-grade relational database",
        "mysql": "Popular open-source relational database",
        "sqlite": "Lightweight embedded database",
        "mongodb": "Document-oriented NoSQL database",
        "mssql": "Microsoft SQL Server database",
        "redis": "In-memory data structure store",
        "memcached": "Distributed memory caching system",
        "dynamodb": "AWS managed NoSQL database",
        "in-memory": "Local memory-based caching",
        "jwt": "JSON Web Token authentication",
        "oauth": "OAuth 2.0 authorization framework",
        "celery": "Distributed task queue",
        "rq": "Simple Redis-based job queue",
        "dramatiq": "Fast and reliable background task processing",
        "arq": "Async job queue with Redis",
        "apscheduler": "Advanced Python scheduler"
    }
    
    service_info = service_descriptions.get(service_type, {})
    provider_desc = provider_descriptions.get(service_provider, "")
    
    features_text = "\n".join([f"• {feature}" for feature in service_info.get("features", [])])
    
    panel_content = (
        f"🎯 [bold]Service Overview:[/bold]\n"
        f"• [cyan]Type[/cyan]: {service_info.get('title', service_type)}\n"
        f"• [cyan]Provider[/cyan]: {service_provider.title()} - {provider_desc}\n"
        f"• [cyan]Description[/cyan]: {service_info.get('description', '')}\n\n"
        f"✨ [bold]Features Included:[/bold]\n{features_text}"
    )
    
    return Panel(
        panel_content,
        title="[bold bright_green]✨ Service Features[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )


def add_service(
    service_type: Optional[str] = typer.Argument(
        None,
        help="🔧 Service type: db | cache | auth | jobs",
        metavar="SERVICE_TYPE"
    ),
    service_provider: Optional[str] = typer.Argument(
        None,
        help="⚙️  Provider: postgresql|mysql|sqlite|mongodb|mssql|redis|memcached|in-memory|jwt|oauth|celery|rq|apscheduler|dramatiq|arq",
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
        • Cache (cache)    - Redis, Memcached, In-Memory
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
    # Handle custom help display
    if help_flag:
        display_service_help()
        raise typer.Exit()

    # Enter interactive mode if service or provider not provided
    if service_type is None or service_provider is None:
        console.clear()
        print_ascii_msg()
        
        # Show a brief overview of available services
        welcome_text = Text()
        welcome_text.append("🚀 Welcome to FastKit Service Setup!", style="bold bright_cyan")
        console.print(Align.center(welcome_text))
        console.print(Align.center("[dim]Add production-ready services to your FastAPI project[/dim]"))
        console.print()
        
        # Interactive selection
        service_type, service_provider = _interactive_service_selection()
        
        # Completion message
        completion_text = Text()
        completion_text.append("✨ Perfect! ", style="bold bright_green")
        completion_text.append("Let's add this service to your project.", style="bright_white")
        console.print(Align.center(completion_text))
        console.print()
    else:
        console.clear()
        print_ascii_msg()

    # Welcome message for service addition
    service_welcome = Text()
    service_welcome.append("🔧 Adding Service: ", style="bold bright_cyan")
    service_welcome.append(f"'{service_type}'", style="bold bright_green")
    service_welcome.append(f" ({service_provider})", style="bright_white")
    service_welcome.append(" to your FastAPI project", style="bright_white")
    
    console.print(Align.center(service_welcome))
    console.print()
    
    # Show service info panel
    service_info = _get_service_info_panel(service_type, service_provider)
    console.print(service_info)
    console.print()

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
        console.print(
            "[bold bright_cyan]📖 Available Services Guide:[/bold bright_cyan]\n")

        # Display service overview tables
        service_panels = create_service_overview_table()

        # Display in 2x2 grid
        top_row = Columns(
            [service_panels[0], service_panels[1]], equal=True, expand=True)
        bottom_row = Columns(
            [service_panels[2], service_panels[3]], equal=True, expand=True)

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

    # Beautiful summary with card-style layout
    console.print("[bold bright_cyan]📋 Service Configuration[/bold bright_cyan]")
    console.print()
    
    # Create elegant summary content
    summary_content = Text()
    
    summary_content.append("🔧  ", style="bright_green")
    summary_content.append("Service: ", style="bold white")
    summary_content.append(f"{service_type}", style="bright_green")
    summary_content.append("\n")
    
    summary_content.append("⚙️   ", style="bright_blue")
    summary_content.append("Provider: ", style="bold white")
    summary_content.append(f"{service_provider}", style="bright_blue")
    summary_content.append("\n")
    
    summary_content.append("📁  ", style="bright_yellow")
    summary_content.append("Project: ", style="bold white")
    summary_content.append(f"{project_path.name}", style="bright_yellow")
    summary_content.append("\n")
    
    summary_content.append("📝  ", style="bright_magenta")
    summary_content.append("Integration: ", style="bold white")
    summary_content.append("Automatic configuration & dependencies", style="bright_magenta")
    summary_content.append("\n\n")
    
    summary_content.append("📦  ", style="bright_cyan")
    summary_content.append("Generated Files: ", style="bold white")
    summary_content.append("client, config, dependencies, examples", style="bright_cyan")
    
    summary_panel = Panel(
        summary_content,
        title="[bold bright_green]✨ Service Summary[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )
    console.print(summary_panel)
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

        # Success message with next steps
        console.print()
        success_panel = Panel(
            f"🎉 [bold bright_green]Success![/bold bright_green] {service_type.title()} service ({service_provider}) has been added.\n\n"
            f"📁 [bold]Service Location:[/bold] [cyan]app/{service_type}/[/cyan]\n\n"
            f"🚀 [bold]Integration Status:[/bold]\n"
            f"  • [bright_blue]Service files created[/bright_blue]\n"
            f"  • [bright_blue]Configuration updated[/bright_blue]\n"
            f"  • [bright_blue]Dependencies synced[/bright_blue]\n"
            f"  • [bright_blue]Examples included[/bright_blue]\n\n"
            + _get_next_steps_text(service_type, service_provider),
            title="[bold bright_green]✨ Service Added Successfully![/bold bright_green]",
            border_style="bright_green",
            padding=(1, 2)
        )
        console.print(success_panel)
        
        # Additional tips
        console.print(
            "[dim]💡 Tip: Check the generated examples and configuration files for usage patterns.[/dim]")
        console.print(
            "[dim]💡 Tip: Update your environment variables as needed for the service connection.[/dim]")
        console.print(
            "\n[bold bright_cyan]Happy coding with your new service! 🚀[/bold bright_cyan]")


    except Exception as e:
        console.print(
            f"\n[bold red]Error adding service:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


def _is_valid_fastkit_project(project_path: Path) -> bool:
    """Check if the current directory is a valid FastKit project."""
    # Delegate to the central detector used across generators
    try:
        from fastkit.shared.project_utils import is_valid_fastkit_project
        return is_valid_fastkit_project(project_path)
    except Exception:
        return False


def _is_valid_service_combination(service_type: str, service_provider: str) -> bool:
    """Validate service type and provider combination."""
    valid_combinations = {
        "db": ["postgresql", "mysql", "sqlite", "mongodb", "mssql"],
        "cache": ["redis", "memcached", "in-memory"],
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


def _get_next_steps_text(service_type: str, service_provider: str) -> str:
    """Get next steps text after adding a service."""
    steps = []
    
    if service_type == "db":
        steps = [
            f"1. [bright_blue]Update environment variables[/bright_blue] for {service_provider} connection",
            "2. [bright_blue]Create database models[/bright_blue] in [cyan]app/models/[/cyan]",
            "3. [bright_blue]Run database migrations[/bright_blue] if needed",
            "4. [bright_blue]Update dependencies[/bright_blue] in [cyan]app/core/dependencies.py[/cyan]"
        ]
    elif service_type == "cache":
        steps = [
            f"1. [bright_blue]Update environment variables[/bright_blue] for {service_provider} connection",
            "2. [bright_blue]Import cache client[/bright_blue]: [cyan]from app.cache import cache_client[/cyan]",
            "3. [bright_blue]Update Docker Compose[/bright_blue] if using containerized development"
        ]
    elif service_type == "auth":
        steps = [
            f"1. [bright_blue]Update environment variables[/bright_blue] for {service_provider} configuration",
            "2. [bright_blue]Create user models[/bright_blue] and authentication endpoints",
            "3. [bright_blue]Update dependencies[/bright_blue] in [cyan]app/core/dependencies.py[/cyan]",
            "4. [bright_blue]Protect routes[/bright_blue] with authentication decorators"
        ]
    elif service_type == "jobs":
        steps = [
            "1. [bright_blue]Review example tasks[/bright_blue] in [cyan]app/jobs/tasks.py[/cyan]",
            "2. [bright_blue]Create custom tasks[/bright_blue] using the @task decorator",
            "3. [bright_blue]Configure job schedules[/bright_blue] (cron, interval, one-time)"
        ]
        
        if service_provider in ["celery", "rq", "dramatiq", "arq"]:
            steps.extend([
                "4. [bright_blue]Start Redis server[/bright_blue] for job queue backend",
                f"5. [bright_blue]Start {service_provider} worker[/bright_blue] to process jobs"
            ])
        elif service_provider == "apscheduler":
            steps.append("4. [bright_blue]Call scheduler.start()[/bright_blue] in application startup")
        
        steps.append("6. [bright_blue]Monitor job execution[/bright_blue] and handle failures")
    
    steps.append("\n7. [bright_blue]Restart your application[/bright_blue] to apply changes")
    
    next_steps_text = "🚀 [bold]Next Steps:[/bold]\n" + "\n".join([f"  {step}" for step in steps])
    return next_steps_text
