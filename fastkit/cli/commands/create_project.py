import os
import typer
from pathlib import Path
from typing import Optional
from InquirerPy import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

from fastkit.shared.project_utils import is_valid_fastkit_project
from fastkit.shared.ui import print_ascii_msg, show_loading_animation
from fastkit.generators.project_generator import scaffold_project_structure
from fastkit.generators.cleanup_utils import cleanup_existing_project


console = Console()


def _create_architecture_info_panel():
    """Create a beautiful panel explaining architecture choices."""
    arch_content = Text()

    # REST API Service
    arch_content.append("🏗️  ", style="bright_green")
    arch_content.append("REST API Service", style="bold bright_green")
    arch_content.append("\n   Perfect for: ", style="dim")
    arch_content.append(
        "Single service APIs, microservice components", style="white")
    arch_content.append("\n   Features: ", style="dim")
    arch_content.append(
        "Clean domain structure, fast setup, production-ready\n\n", style="cyan")

    # Fullstack Application
    arch_content.append("🌐  ", style="bright_blue")
    arch_content.append("Fullstack Application", style="bold bright_blue")
    arch_content.append("\n   Perfect for: ", style="dim")
    arch_content.append(
        "Web applications with frontend and backend", style="white")
    arch_content.append("\n   Features: ", style="dim")
    arch_content.append(
        "Backend + Frontend + Infrastructure setup\n\n", style="cyan")

    # Microservices
    arch_content.append("🔗  ", style="bright_magenta")
    arch_content.append("Microservices Architecture",
                        style="bold bright_magenta")
    arch_content.append("\n   Perfect for: ", style="dim")
    arch_content.append(
        "Distributed systems, enterprise applications", style="white")
    arch_content.append("\n   Features: ", style="dim")
    arch_content.append(
        "Multiple services, API gateway, service mesh\n\n", style="cyan")

    return Panel(
        arch_content,
        title="[bold bright_cyan]🏛️  Choose Your Architecture[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )


def _create_database_info_panel():
    """Create a beautiful panel explaining database choices."""
    db_content = Text()

    # PostgreSQL
    db_content.append("🐘  ", style="bright_blue")
    db_content.append("PostgreSQL", style="bold bright_blue")
    db_content.append(" (SQL) ", style="dim")
    db_content.append("⭐⭐⭐⭐⭐", style="yellow")
    db_content.append("\n   Best for: ", style="dim")
    db_content.append(
        "Production applications, complex queries, ACID compliance", style="white")
    db_content.append("\n   Why choose: ", style="dim")
    db_content.append(
        "Industry standard, excellent performance, rich features\n\n", style="cyan")

    # MySQL
    db_content.append("🐬  ", style="bright_green")
    db_content.append("MySQL", style="bold bright_green")
    db_content.append(" (SQL) ", style="dim")
    db_content.append("⭐⭐⭐⭐", style="yellow")
    db_content.append("\n   Best for: ", style="dim")
    db_content.append(
        "Web applications, high compatibility, shared hosting", style="white")
    db_content.append("\n   Why choose: ", style="dim")
    db_content.append(
        "Widely supported, fast reads, easy to deploy\n\n", style="cyan")

    # SQLite
    db_content.append("📁  ", style="bright_yellow")
    db_content.append("SQLite", style="bold bright_yellow")
    db_content.append(" (SQL) ", style="dim")
    db_content.append("⭐⭐⭐", style="yellow")
    db_content.append("\n   Best for: ", style="dim")
    db_content.append(
        "Development, prototyping, small applications", style="white")
    db_content.append("\n   Why choose: ", style="dim")
    db_content.append(
        "Zero configuration, file-based, perfect for testing\n\n", style="cyan")

    # MongoDB
    db_content.append("🍃  ", style="bright_green")
    db_content.append("MongoDB", style="bold bright_green")
    db_content.append(" (NoSQL) ", style="dim")
    db_content.append("⭐⭐⭐⭐", style="yellow")
    db_content.append("\n   Best for: ", style="dim")
    db_content.append(
        "Document storage, flexible schemas, rapid development", style="white")
    db_content.append("\n   Why choose: ", style="dim")
    db_content.append(
        "Schema flexibility, horizontal scaling, JSON-like documents\n\n", style="cyan")

    # SQL Server
    db_content.append("🏢  ", style="bright_blue")
    db_content.append("SQL Server", style="bold bright_blue")
    db_content.append(" (SQL) ", style="dim")
    db_content.append("⭐⭐⭐⭐", style="yellow")
    db_content.append("\n   Best for: ", style="dim")
    db_content.append(
        "Enterprise applications, Windows environments, Microsoft stack", style="white")
    db_content.append("\n   Why choose: ", style="dim")
    db_content.append(
        "Enterprise features, excellent tooling, Windows integration", style="cyan")

    return Panel(
        db_content,
        title="[bold bright_blue]🗄️  Database Options[/bold bright_blue]",
        border_style="bright_blue",
        padding=(1, 2)
    )


def _create_cache_info_panel():
    """Create a beautiful panel explaining cache choices."""
    cache_content = Text()

    # Redis
    cache_content.append("🔴  ", style="bright_red")
    cache_content.append("Redis", style="bold bright_red")
    cache_content.append(" (In-Memory) ", style="dim")
    cache_content.append("🚀🚀🚀", style="yellow")
    cache_content.append("\n   Best for: ", style="dim")
    cache_content.append(
        "High-performance caching, pub/sub, session storage", style="white")
    cache_content.append("\n   Why choose: ", style="dim")
    cache_content.append(
        "Lightning fast, rich data types, persistence options\n\n", style="cyan")

    # Memcached
    cache_content.append("💾  ", style="bright_blue")
    cache_content.append("Memcached", style="bold bright_blue")
    cache_content.append(" (Distributed) ", style="dim")
    cache_content.append("🚀🚀", style="yellow")
    cache_content.append("\n   Best for: ", style="dim")
    cache_content.append(
        "Simple caching, horizontal scaling, memory efficiency", style="white")
    cache_content.append("\n   Why choose: ", style="dim")
    cache_content.append(
        "Simple setup, excellent for basic caching needs\n\n", style="cyan")

    # In-Memory
    cache_content.append("🧠  ", style="bright_green")
    cache_content.append("In-Memory", style="bold bright_green")
    cache_content.append(" (Local) ", style="dim")
    cache_content.append("🚀", style="yellow")
    cache_content.append("\n   Best for: ", style="dim")
    cache_content.append(
        "Development, testing, single-instance applications", style="white")
    cache_content.append("\n   Why choose: ", style="dim")
    cache_content.append(
        "Zero external dependencies, perfect for development", style="cyan")

    return Panel(
        cache_content,
        title="[bold bright_magenta]⚡ Cache Options[/bold bright_magenta]",
        border_style="bright_magenta",
        padding=(1, 2)
    )


def _create_auth_info_panel():
    """Create a beautiful panel explaining auth choices."""
    auth_content = Text()

    # JWT
    auth_content.append("🎫  ", style="bright_blue")
    auth_content.append("JWT (JSON Web Tokens)", style="bold bright_blue")
    auth_content.append(" ", style="dim")
    auth_content.append("🔒🔒🔒", style="yellow")
    auth_content.append("\n   Best for: ", style="dim")
    auth_content.append(
        "REST APIs, stateless authentication, microservices", style="white")
    auth_content.append("\n   Why choose: ", style="dim")
    auth_content.append(
        "Stateless, scalable, industry standard for APIs\n\n", style="cyan")

    # OAuth 2.0
    auth_content.append("🌐  ", style="bright_green")
    auth_content.append("OAuth 2.0", style="bold bright_green")
    auth_content.append(" ", style="dim")
    auth_content.append("🔒🔒🔒🔒", style="yellow")
    auth_content.append("\n   Best for: ", style="dim")
    auth_content.append(
        "Social login, third-party integrations, enterprise SSO", style="white")
    auth_content.append("\n   Why choose: ", style="dim")
    auth_content.append(
        "Secure delegation, social providers, enterprise ready\n\n", style="cyan")

    # None
    auth_content.append("🔓  ", style="dim")
    auth_content.append("No Authentication", style="bold dim")
    auth_content.append("\n   Best for: ", style="dim")
    auth_content.append(
        "Public APIs, development, open data services", style="white")
    auth_content.append("\n   Why choose: ", style="dim")
    auth_content.append(
        "Simple setup, no user management complexity", style="cyan")

    return Panel(
        auth_content,
        title="[bold bright_red]🔐 Authentication Options[/bold bright_red]",
        border_style="bright_red",
        padding=(1, 2)
    )


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
        "memcached": "memcached",
        "in-memory": "in-memory",
        "memory": "in-memory",
        "local": "in-memory",
        "none": "none",
    }
    return mapping.get(cache_choice.lower(), cache_choice.lower())


def _normalize_architecture_choice(architecture: str) -> str:
    mapping = {
        "fullstack application": "fullstack",
        "microservices architecture": "microservices",
        "rest api service": "rest-apis",
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


def create_project(
    project_name: Optional[str] = typer.Argument(
        None,
        help="🏷️  Name of the project to create (e.g., my-awesome-api)",
        metavar="PROJECT_NAME"
    ),
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="📁 Directory to create the project in (default: current directory)",
        metavar="PATH"
    ),
):
    """
    🏗️  Create a new FastAPI project with modern architecture patterns.

    This command creates a complete FastAPI project structure with your choice of:

    🏛️  ARCHITECTURES:
        • REST API Service     - Single service with clean domain structure
        • Fullstack App        - Backend + Frontend + Infrastructure
        • Microservices        - Multiple services with API gateway

    🔧 INTEGRATIONS:
        • Database: PostgreSQL, MySQL, SQLite, MongoDB, SQL Server
        • Cache: Redis, Memcached, In-Memory
        • Auth: JWT tokens, OAuth 2.0
        • CI/CD: GitHub Actions workflows
        • Docker: Multi-stage builds and compose files

    📋 EXAMPLES:
        fastkit create-project my-api
        fastkit create-project blog-app --path ~/projects
        fastkit create-project ecommerce-backend
    """
    console.clear()
    print_ascii_msg()

    # Welcome message with beautiful styling
    welcome_text = Text()
    welcome_text.append(
        "🚀 Welcome to FastKit Project Creator! ", style="bold bright_cyan")
    welcome_text.append(
        "Let's build something amazing together.", style="bright_white")

    console.print(Align.center(welcome_text))
    console.print()

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
        # Check if it's a FastKit project
        is_fastkit = is_valid_fastkit_project(target_dir)

        if is_fastkit:
            console.print(
                f"[yellow]⚠️  FastKit project detected in '{target_dir}'[/yellow]")
            overwrite = typer.confirm(
                "This will completely replace the existing FastKit project with a new one. All current files will be removed. Continue?",
                default=False
            )
        else:
            console.print(
                f"[yellow]⚠️  Directory '{target_dir}' is not empty[/yellow]")
            overwrite = typer.confirm(
                "This will clean up the directory and create a new FastKit project. Continue?",
                default=False
            )

        if not overwrite:
            typer.echo("Aborting.")
            raise typer.Exit(code=1)
        else:
            # Clean up the existing project directory
            if is_fastkit:
                console.print(
                    "[yellow]🧹 Cleaning up existing FastKit project...[/yellow]")
            else:
                console.print("[yellow]🧹 Cleaning up directory...[/yellow]")

            cleanup_existing_project(target_dir)
            console.print("[green]✓ Cleanup completed[/green]")
            console.print()

    # Show architecture guide
    console.print(
        "[bold bright_cyan]🏠 Step 1: Choose Your Architecture[/bold bright_cyan]")
    console.print()
    arch_panel = _create_architecture_info_panel()
    console.print(arch_panel)
    console.print()

    architecture = _normalize_architecture_choice(
        _prompt_with_choices(
            "🏛️ Select project architecture",
            [
                "REST API Service",
                "Fullstack Application",
                "Microservices Architecture"
            ],
            default="REST API Service",
        )
    )
    console.print(f"[dim]✓ Selected: {architecture}[/dim]")
    console.print()

    # Authentication setup
    console.print(
        "[bold bright_red]🔐 Step 2: Authentication Setup[/bold bright_red]")
    console.print()
    auth_panel = _create_auth_info_panel()
    console.print(auth_panel)
    console.print()

    needs_auth = typer.confirm(
        "🔒 Do you want to include authentication?", default=False)
    auth_type = "none"
    if needs_auth:
        auth_type = _prompt_with_choices("🔐 Choose authentication type", [
                                         "jwt", "oauth"], default="jwt")
        console.print(f"[dim]✓ Selected: {auth_type}[/dim]")
    else:
        console.print("[dim]✓ No authentication selected[/dim]")
    console.print()

    # Database setup
    console.print(
        "[bold bright_blue]🗄️ Step 3: Database Integration[/bold bright_blue]")
    console.print()
    db_panel = _create_database_info_panel()
    console.print(db_panel)
    console.print()

    db_choice = "none"
    if typer.confirm("🗄️ Add a database integration?", default=True):
        db_choice = _normalize_db_choice(
            _prompt_with_choices(
                "Choose a database",
                ["postgresql", "sqlite", "mysql", "mongodb", "mssql"],
                default="sqlite",
            )
        )
        console.print(f"[dim]✓ Selected: {db_choice}[/dim]")
    else:
        console.print("[dim]✓ No database selected[/dim]")
    console.print()

    # Cache setup
    console.print(
        "[bold bright_magenta]⚡ Step 4: Cache Integration[/bold bright_magenta]")
    console.print()
    cache_panel = _create_cache_info_panel()
    console.print(cache_panel)
    console.print()

    cache_choice = "none"
    if typer.confirm("⚡ Add a caching system?", default=False):
        cache_choice = _normalize_cache_choice(
            _prompt_with_choices("Choose a cache provider", [
                                 "redis", "memcached", "in-memory", "none"], default="redis")
        )
        console.print(f"[dim]✓ Selected: {cache_choice}[/dim]")
    else:
        console.print("[dim]✓ No cache selected[/dim]")
    console.print()

    # DevOps setup
    console.print(
        "[bold bright_yellow]🚀 Step 5: DevOps & Deployment[/bold bright_yellow]")
    console.print()

    devops_panel = Panel(
        "🛠️ [bold]DevOps Features:[/bold]\n"
        "• [cyan]CI/CD Pipelines[/cyan] - Automated testing & deployment\n"
        "• [cyan]Docker Setup[/cyan] - Containerization for all environments\n"
        "• [cyan]GitHub Actions[/cyan] - Automated workflows\n"
        "• [cyan]Multi-stage builds[/cyan] - Optimized production images",
        title="[bold bright_yellow]🚀 DevOps Options[/bold bright_yellow]",
        border_style="bright_yellow",
        padding=(1, 1)
    )
    console.print(devops_panel)
    console.print()

    include_cicd = typer.confirm(
        "🛠️ Include CI/CD pipelines (GitHub Actions)?", default=True)
    console.print(f"[dim]✓ CI/CD: {'Yes' if include_cicd else 'No'}[/dim]")

    include_docker = typer.confirm(
        "🐳 Include Docker setup?", default=True)
    console.print(f"[dim]✓ Docker: {'Yes' if include_docker else 'No'}[/dim]")
    console.print()

    # Get architecture-specific configuration
    architecture_config = {}
    if architecture == "microservices":
        architecture_config = _get_microservices_config()

    # Beautiful summary with card-style layout
    console.print("[bold bright_cyan]📋 Final Configuration[/bold bright_cyan]")
    console.print()

    # Create elegant summary content
    summary_content = Text()

    # Project basics
    summary_content.append("🏷️  ", style="bright_cyan")
    summary_content.append("Project: ", style="bold white")
    summary_content.append(f"{project_name}", style="bright_cyan")
    summary_content.append("\n")

    summary_content.append("🏛️  ", style="bright_cyan")
    summary_content.append("Architecture: ", style="bold white")
    summary_content.append(
        f"{architecture.replace('-', ' ').title()}", style="bright_green")
    summary_content.append("\n")

    # Services
    summary_content.append("🔐  ", style="bright_red")
    summary_content.append("Authentication: ", style="bold white")
    auth_display = auth_type.upper() if auth_type != 'none' else 'None'
    summary_content.append(
        f"{auth_display}", style="bright_red" if auth_type != 'none' else "dim")
    summary_content.append("\n")

    summary_content.append("🗄️  ", style="bright_blue")
    summary_content.append("Database: ", style="bold white")
    db_display = db_choice.title() if db_choice != 'none' else 'None'
    summary_content.append(
        f"{db_display}", style="bright_blue" if db_choice != 'none' else "dim")
    summary_content.append("\n")

    summary_content.append("⚡  ", style="bright_magenta")
    summary_content.append("Cache: ", style="bold white")
    cache_display = cache_choice.title() if cache_choice != 'none' else 'None'
    summary_content.append(
        f"{cache_display}", style="bright_magenta" if cache_choice != 'none' else "dim")
    summary_content.append("\n")

    # DevOps
    summary_content.append("🛠️  ", style="bright_yellow")
    summary_content.append("CI/CD: ", style="bold white")
    summary_content.append("Enabled" if include_cicd else "Disabled",
                           style="bright_yellow" if include_cicd else "dim")
    summary_content.append("\n")

    summary_content.append("🐳  ", style="bright_blue")
    summary_content.append("Docker: ", style="bold white")
    summary_content.append("Enabled" if include_docker else "Disabled",
                           style="bright_blue" if include_docker else "dim")

    # Architecture-specific config
    if architecture_config:
        summary_content.append(
            "\n\n[bold]Architecture Configuration:[/bold]\n", style="bright_white")
        if architecture == "microservices":
            services_list = ", ".join(architecture_config.get("services", []))
            summary_content.append("🔍  Services: ", style="bold white")
            summary_content.append(f"{services_list}", style="bright_cyan")
            summary_content.append("\n")
            summary_content.append("🌐  Gateway: ", style="bold white")
            gateway_status = 'Yes' if architecture_config.get(
                "include_gateway") else 'No'
            summary_content.append(
                f"{gateway_status}", style="bright_green" if gateway_status == 'Yes' else "dim")

    summary_panel = Panel(
        summary_content,
        title="[bold bright_green]✨ Your FastAPI Project Configuration[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )
    console.print(summary_panel)
    console.print()
    proceed = typer.confirm(
        "Proceed to create the directory structure?", default=True)
    if not proceed:
        typer.echo("Aborting.")
        raise typer.Exit(code=1)

    show_loading_animation("Creating project structure...")

    scaffold_project_structure(
        base_path=target_dir,
        project_name=project_name,
        architecture=architecture,
        auth_type=auth_type,
        db_choice=db_choice,
        cache_choice=cache_choice,
        architecture_config=architecture_config,
        include_cicd=include_cicd,
        include_docker=include_docker,
    )

    # Success message with next steps
    console.print()
    success_panel = Panel(
        f"🎉 [bold bright_green]Success![/bold bright_green] Your FastAPI project has been created.\n\n"
        f"📁 [bold]Project Location:[/bold] [cyan]{target_dir}[/cyan]\n\n"
        f"🚀 [bold]Next Steps:[/bold]\n"
        f"  1. [bright_blue]cd {project_name}[/bright_blue]\n"
        f"  2. [bright_blue]uv sync[/bright_blue] (install dependencies)\n"
        f"  3. [bright_blue]uv run fastapi dev app/main.py[/bright_blue] (start development server)\n\n"
        f"📚 [bold]Documentation:[/bold] Check the generated README.md for detailed setup instructions",
        title="[bold bright_green]✨ Project Created Successfully![/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )
    console.print(success_panel)

    # Additional tips based on selections
    if db_choice != "none":
        console.print(
            f"[dim]💡 Tip: Don't forget to set up your {db_choice} database connection in the environment variables.[/dim]")

    if cache_choice != "none":
        console.print(
            f"[dim]💡 Tip: Make sure your {cache_choice} server is running before starting the application.[/dim]")

    if include_docker:
        console.print(
            "[dim]💡 Tip: Use 'docker-compose up' to start all services in containers.[/dim]")

    console.print("\n[bold bright_cyan]Happy coding! 🚀[/bold bright_cyan]")
