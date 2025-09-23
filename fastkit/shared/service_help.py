"""Service help utilities for displaying beautiful service information."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

console = Console()


def create_service_overview_table():
    """Create a comprehensive service overview table."""

    # Database services table
    db_table = Table(show_header=True,
                     header_style="bold bright_blue", box=None, padding=(0, 1))
    db_table.add_column("Provider", style="bright_green", min_width=12)
    db_table.add_column("Type", style="cyan", min_width=8)
    db_table.add_column("Best For", style="white", min_width=20)

    db_table.add_row("postgresql", "SQL", "Production apps, complex queries")
    db_table.add_row("mysql", "SQL", "Web apps, high compatibility")
    db_table.add_row("sqlite", "SQL", "Development, small apps")
    db_table.add_row("mongodb", "NoSQL", "Document storage, flexibility")
    db_table.add_row("mssql", "SQL", "Enterprise, Windows environments")

    db_panel = Panel(
        db_table,
        title="[bold bright_blue]🗄️  Database Services (db)[/bold bright_blue]",
        border_style="bright_blue",
        padding=(1, 1)
    )

    # Cache services table
    cache_table = Table(
        show_header=True, header_style="bold bright_magenta", box=None, padding=(0, 1))
    cache_table.add_column("Provider", style="bright_green", min_width=12)
    cache_table.add_column("Type", style="cyan", min_width=12)
    cache_table.add_column("Best For", style="white", min_width=20)

    cache_table.add_row("redis", "In-Memory", "High performance, pub/sub")
    cache_table.add_row("memcached", "Distributed",
                        "Simple caching, scalability")
    cache_table.add_row("dynamodb", "Cloud", "AWS environments, serverless")
    cache_table.add_row("in-memory", "Local", "Development, testing")

    cache_panel = Panel(
        cache_table,
        title="[bold bright_magenta]⚡ Cache Services (cache)[/bold bright_magenta]",
        border_style="bright_magenta",
        padding=(1, 1)
    )

    # Auth services table
    auth_table = Table(
        show_header=True, header_style="bold bright_red", box=None, padding=(0, 1))
    auth_table.add_column("Provider", style="bright_green", min_width=12)
    auth_table.add_column("Type", style="cyan", min_width=12)
    auth_table.add_column("Best For", style="white", min_width=20)

    auth_table.add_row("jwt", "Token-based", "APIs, stateless auth")
    auth_table.add_row("oauth", "OAuth 2.0", "Social login, third-party")

    auth_panel = Panel(
        auth_table,
        title="[bold bright_red]🔐 Auth Services (auth)[/bold bright_red]",
        border_style="bright_red",
        padding=(1, 1)
    )

    # Jobs services table
    jobs_table = Table(
        show_header=True, header_style="bold bright_green", box=None, padding=(0, 1))
    jobs_table.add_column("Provider", style="bright_green", min_width=12)
    jobs_table.add_column("Type", style="cyan", min_width=12)
    jobs_table.add_column("Best For", style="white", min_width=20)

    jobs_table.add_row("celery", "Distributed",
                       "Production, complex workflows")
    jobs_table.add_row("rq", "Simple", "Lightweight, Redis-based")
    jobs_table.add_row("dramatiq", "Modern", "Reliable, actor-based")
    jobs_table.add_row("arq", "Async", "FastAPI-friendly, async/await")
    jobs_table.add_row("apscheduler", "Scheduler", "Cron-like, in-process")

    jobs_panel = Panel(
        jobs_table,
        title="[bold bright_green]⚙️  Job Services (jobs)[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 1)
    )

    return [db_panel, cache_panel, auth_panel, jobs_panel]


def create_service_examples_panel():
    """Create a panel with practical service examples."""

    examples_content = Text()

    # Database examples
    examples_content.append("🗄️  DATABASE EXAMPLES:\n",
                            style="bold bright_blue")
    examples_content.append(
        "   fastkit add-service db postgresql", style="bright_green")
    examples_content.append("  # Production PostgreSQL\n", style="dim")
    examples_content.append(
        "   fastkit add-service db sqlite", style="bright_green")
    examples_content.append("      # Development SQLite\n", style="dim")
    examples_content.append(
        "   fastkit add-service db mongodb", style="bright_green")
    examples_content.append("      # NoSQL document store\n\n", style="dim")

    # Cache examples
    examples_content.append("⚡ CACHE EXAMPLES:\n", style="bold bright_magenta")
    examples_content.append(
        "   fastkit add-service cache redis", style="bright_green")
    examples_content.append("       # High-performance caching\n", style="dim")
    examples_content.append(
        "   fastkit add-service cache in-memory", style="bright_green")
    examples_content.append("   # Local development\n\n", style="dim")

    # Auth examples
    examples_content.append("🔐 AUTH EXAMPLES:\n", style="bold bright_red")
    examples_content.append(
        "   fastkit add-service auth jwt", style="bright_green")
    examples_content.append("         # Token-based auth\n", style="dim")
    examples_content.append(
        "   fastkit add-service auth oauth", style="bright_green")
    examples_content.append("       # Social login\n\n", style="dim")

    # Jobs examples
    examples_content.append("⚙️  JOBS EXAMPLES:\n", style="bold bright_green")
    examples_content.append(
        "   fastkit add-service jobs celery", style="bright_green")
    examples_content.append("      # Production task queue\n", style="dim")
    examples_content.append(
        "   fastkit add-service jobs arq", style="bright_green")
    examples_content.append("         # Async job processing\n", style="dim")

    return Panel(
        examples_content,
        title="[bold bright_cyan]📋 Quick Examples[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )


def create_service_usage_guide():
    """Create a usage guide panel."""

    usage_content = Text()
    usage_content.append("1. Choose service type: ", style="white")
    usage_content.append("db", style="bold bright_blue")
    usage_content.append(" | ", style="dim")
    usage_content.append("cache", style="bold bright_magenta")
    usage_content.append(" | ", style="dim")
    usage_content.append("auth", style="bold bright_red")
    usage_content.append(" | ", style="dim")
    usage_content.append("jobs", style="bold bright_green")
    usage_content.append("\n\n", style="white")

    usage_content.append(
        "2. Select provider from the tables above\n\n", style="white")

    usage_content.append("3. Run command: ", style="white")
    usage_content.append(
        "fastkit add-service <type> <provider>", style="bold bright_cyan")
    usage_content.append("\n\n", style="white")

    usage_content.append("💡 ", style="yellow")
    usage_content.append("Tip: Use ", style="white")
    usage_content.append("--help", style="bold bright_blue")
    usage_content.append(
        " with any command for detailed information", style="white")

    return Panel(
        usage_content,
        title="[bold bright_cyan]🚀 How to Use[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )


def display_service_help():
    """Display comprehensive service help."""
    console.clear()

    # Title
    console.print()
    console.print(
        "[bold bright_cyan]🔧 FastKit Service Guide[/bold bright_cyan]", justify="center")
    console.print(
        "[dim]Add production-ready services to your FastAPI project[/dim]", justify="center")
    console.print()

    # Service overview tables
    service_panels = create_service_overview_table()

    # Display in 2x2 grid
    top_row = Columns([service_panels[0], service_panels[1]],
                      equal=True, expand=True)
    bottom_row = Columns(
        [service_panels[2], service_panels[3]], equal=True, expand=True)

    console.print(top_row)
    console.print()
    console.print(bottom_row)
    console.print()

    # Examples and usage guide
    examples_panel = create_service_examples_panel()
    usage_panel = create_service_usage_guide()

    guide_row = Columns([examples_panel, usage_panel], equal=True, expand=True)
    console.print(guide_row)
    console.print()


def create_domain_examples_panel():
    """Create a panel with domain examples."""

    examples_content = Text()

    # Common business domains
    examples_content.append("🏢 BUSINESS DOMAINS:\n", style="bold bright_cyan")
    examples_content.append(
        "   fastkit add-domain users", style="bright_green")
    examples_content.append(
        "        # User management & profiles\n", style="dim")
    examples_content.append(
        "   fastkit add-domain products", style="bright_green")
    examples_content.append(
        "     # Product catalog & inventory\n", style="dim")
    examples_content.append(
        "   fastkit add-domain orders", style="bright_green")
    examples_content.append(
        "       # Order processing & fulfillment\n", style="dim")
    examples_content.append(
        "   fastkit add-domain payments", style="bright_green")
    examples_content.append("     # Payment processing\n\n", style="dim")

    # Technical domains
    examples_content.append("🔧 TECHNICAL DOMAINS:\n", style="bold bright_blue")
    examples_content.append(
        "         # Authentication & authorization\n", style="dim")
    examples_content.append(
        "   fastkit add-domain analytics", style="bright_green")
    examples_content.append("    # Analytics & reporting\n", style="dim")
    examples_content.append(
        "   fastkit add-domain notifications", style="bright_green")
    examples_content.append(" # Email, SMS, push notifications\n", style="dim")

    return Panel(
        examples_content,
        title="[bold bright_cyan]📋 Domain Examples[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )


def create_domain_structure_panel():
    """Create a panel showing domain structure."""

    structure_content = Text()
    structure_content.append("📁 GENERATED FILES:\n", style="bold bright_green")
    structure_content.append("   models.py", style="bright_blue")
    structure_content.append(
        "       # Database models (SQLAlchemy/Motor)\n", style="dim")
    structure_content.append("   schemas.py", style="bright_blue")
    structure_content.append(
        "      # Pydantic schemas for validation\n", style="dim")
    structure_content.append("   services.py", style="bright_blue")
    structure_content.append(
        "     # Business logic & domain services\n", style="dim")
    structure_content.append("   repositories.py", style="bright_blue")
    structure_content.append(" # Data access layer\n", style="dim")
    structure_content.append("   routes.py", style="bright_blue")
    structure_content.append(
        "       # API endpoints for the domain\n", style="dim")
    structure_content.append("   dependencies.py", style="bright_blue")
    structure_content.append(" # Domain-specific dependencies\n", style="dim")
    structure_content.append("   exceptions.py", style="bright_blue")
    structure_content.append(
        "   # Domain-specific exceptions\n\n", style="dim")

    structure_content.append("🎯 AUTO-INTEGRATION:\n",
                             style="bold bright_yellow")
    structure_content.append("   • Routes available at ", style="white")
    structure_content.append("/api/v1/{domain}s", style="bold bright_cyan")
    structure_content.append(
        "\n   • Clean architecture patterns\n", style="white")
    structure_content.append(
        "   • Test files included (optional)\n", style="white")

    return Panel(
        structure_content,
        title="[bold bright_green]🏗️  Domain Structure[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )


def display_domain_help():
    """Display comprehensive domain help."""
    console.clear()

    # Title
    console.print()
    console.print(
        "[bold bright_cyan]🏢 FastKit Domain Guide[/bold bright_cyan]", justify="center")
    console.print(
        "[dim]Add business domains with clean architecture patterns[/dim]", justify="center")
    console.print()

    # Examples and structure
    examples_panel = create_domain_examples_panel()
    structure_panel = create_domain_structure_panel()

    guide_row = Columns([examples_panel, structure_panel],
                        equal=True, expand=True)
    console.print(guide_row)
    console.print()

    # Usage guide
    usage_content = Text()
    usage_content.append("🚀 USAGE:\n", style="bold bright_cyan")
    usage_content.append("   fastkit add-domain <name>",
                         style="bold bright_green")
    usage_content.append("           # Add domain with tests\n", style="dim")
    usage_content.append(
        "   fastkit add-domain <name> --no-tests", style="bold bright_green")
    usage_content.append("  # Skip test files\n", style="dim")
    usage_content.append(
        "   fastkit add-domain <name> --force", style="bold bright_green")
    usage_content.append("       # Overwrite existing\n\n", style="dim")

    usage_content.append("💡 ", style="yellow")
    usage_content.append(
        "Domain names should be lowercase, descriptive, and represent\n", style="white")
    usage_content.append(
        "   a clear business area or feature set in your application.", style="white")

    usage_panel = Panel(
        usage_content,
        title="[bold bright_cyan]📖 Usage Guide[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )

    console.print(usage_panel)
    console.print()
