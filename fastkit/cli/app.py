import typer
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table

from fastkit.shared.ui import *
from fastkit.shared.service_help import display_service_help, display_domain_help
from fastkit.cli.commands.greet import greet
from fastkit.cli.commands.version import version
from fastkit.cli.commands.create_project import create_project
from fastkit.cli.commands.add_domain import add_domain
from fastkit.cli.commands.add_service import add_service

app = typer.Typer(
    name="fastkit",
    help="🚀 FastKit CLI - Lightning Fast FastAPI Development",
    add_completion=False,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]}
)
console = Console()


def create_help():
    """Create a beautiful, organized help display"""
    console.clear()
    print_ascii_msg()

    # Main description
    description = Text()
    description.append(
        "A modern CLI toolkit for scaffolding FastAPI projects with production-ready\n", style="white")
    description.append(
        "templates, integrations, and best practices.\n", style="white")
    console.print(Align.center(description))
    console.print()

    # Commands section
    commands_table = Table(
        show_header=True, header_style="bold bright_cyan", box=None, padding=(0, 2))
    commands_table.add_column(
        "Command", style="bold bright_blue", min_width=20)
    commands_table.add_column("Description", style="white", min_width=50)

    commands_table.add_row(
        "create-project",
        "Create a new FastAPI project with architecture options"
    )
    commands_table.add_row(
        "add-service",
        "Add services (database, cache, auth, jobs) to existing project"
    )
    commands_table.add_row(
        "add-domain",
        "Add business domain with models, services, and routes"
    )
    commands_table.add_row(
        "version",
        "Show FastKit version and system information"
    )
    commands_table.add_row(
        "greet",
        "Greet someone with style (demo command)"
    )

    commands_panel = Panel(
        commands_table,
        title="[bold bright_cyan]📋 Available Commands[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )
    console.print(commands_panel)
    console.print()

    # Quick start examples
    examples_content = Text()
    examples_content.append("# Create a new project\n", style="dim")
    examples_content.append(
        "fastkit create-project my-awesome-api\n\n", style="bold bright_green")

    examples_content.append("# Add database service\n", style="dim")
    examples_content.append(
        "fastkit add-service db postgresql\n\n", style="bold bright_green")

    examples_content.append("# Add caching service\n", style="dim")
    examples_content.append(
        "fastkit add-service cache redis\n\n", style="bold bright_green")

    examples_content.append("# Add authentication\n", style="dim")
    examples_content.append(
        "fastkit add-service auth jwt\n\n", style="bold bright_green")

    examples_content.append("# Add business domain\n", style="dim")
    examples_content.append("fastkit add-domain users\n",
                            style="bold bright_green")

    examples_panel = Panel(
        examples_content,
        title="[bold bright_green]🚀 Quick Start Examples[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )
    console.print(examples_panel)
    console.print()

    # Services overview
    services_columns = []

    # Database services
    db_table = Table(show_header=True, header_style="bold yellow", box=None)
    db_table.add_column("Database", style="bright_blue")
    db_table.add_column("Type", style="white")
    db_table.add_row("postgresql", "SQL")
    db_table.add_row("mysql", "SQL")
    db_table.add_row("sqlite", "SQL")
    db_table.add_row("mongodb", "NoSQL")
    db_table.add_row("mssql", "SQL")

    db_panel = Panel(
        db_table,
        title="[bold yellow]🗄️  Database[/bold yellow]",
        border_style="yellow",
        width=25
    )
    services_columns.append(db_panel)

    # Cache services
    cache_table = Table(
        show_header=True, header_style="bold magenta", box=None)
    cache_table.add_column("Cache", style="bright_blue")
    cache_table.add_column("Type", style="white")
    cache_table.add_row("redis", "In-Memory")
    cache_table.add_row("memcached", "Distributed")
    cache_table.add_row("in-memory", "Local")

    cache_panel = Panel(
        cache_table,
        title="[bold magenta]⚡ Cache[/bold magenta]",
        border_style="magenta",
        width=25
    )
    services_columns.append(cache_panel)

    # Auth services
    auth_table = Table(show_header=True, header_style="bold red", box=None)
    auth_table.add_column("Auth", style="bright_blue")
    auth_table.add_column("Type", style="white")
    auth_table.add_row("jwt", "Token-based")
    auth_table.add_row("oauth", "OAuth 2.0")

    auth_panel = Panel(
        auth_table,
        title="[bold red]🔐 Authentication[/bold red]",
        border_style="red",
        width=25
    )
    services_columns.append(auth_panel)

    # Jobs services
    jobs_table = Table(show_header=True, header_style="bold green", box=None)
    jobs_table.add_column("Jobs", style="bright_blue")
    jobs_table.add_column("Type", style="white")
    jobs_table.add_row("celery", "Distributed")
    jobs_table.add_row("rq", "Simple")
    jobs_table.add_row("dramatiq", "Modern")
    jobs_table.add_row("arq", "Async")
    jobs_table.add_row("apscheduler", "Scheduler")

    jobs_panel = Panel(
        jobs_table,
        title="[bold green]⚙️  Background Jobs[/bold green]",
        border_style="green",
        width=25
    )
    services_columns.append(jobs_panel)

    services_overview = Panel(
        Columns(services_columns, equal=True, expand=True),
        title="[bold bright_cyan]🛠️  Available Services[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 1)
    )
    console.print(services_overview)
    console.print()

    # Options section
    options_content = Text()
    options_content.append("-h, --help", style="bold bright_blue")
    options_content.append(
        "     Show this help message and exit\n", style="white")
    options_content.append("--version", style="bold bright_blue")
    options_content.append("      Show version information\n", style="white")

    options_panel = Panel(
        options_content,
        title="[bold bright_cyan]⚙️  Global Options[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )
    console.print(options_panel)
    console.print()

    # Footer with links
    footer_content = Text()
    footer_content.append("📚 Documentation: ", style="white")
    footer_content.append(
        "https://github.com/TechHubHQ/fastkit\n", style="bright_blue underline")
    footer_content.append("🐛 Issues & Support: ", style="white")
    footer_content.append(
        "https://github.com/TechHubHQ/fastkit/issues\n", style="bright_blue underline")
    footer_content.append("💡 Get command help: ", style="white")
    footer_content.append("fastkit <command> --help",
                          style="bold bright_green")

    footer_panel = Panel(
        footer_content,
        title="[bold bright_cyan]📖 Documentation & Support[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )
    console.print(footer_panel)
    console.print()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version_flag: bool = typer.Option(
        False,
        "--version",
        help="Show version information and exit",
        is_eager=True
    ),
    help_flag: bool = typer.Option(
        False,
        "--help",
        "-h",
        help="Show this help message and exit",
        is_eager=True
    ),
):
    """
    🚀 FastKit CLI - Lightning Fast FastAPI Development

    A modern CLI toolkit for scaffolding FastAPI projects with production-ready
    templates, integrations, and best practices.
    """

    if version_flag:
        # Show version using the version command
        version()
        raise typer.Exit()

    if help_flag:
        create_help()
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        # Clear screen for clean presentation
        console.clear()

        # Display the main interface
        print_ascii_msg()

        # Welcome message
        welcome_text = Text()
        welcome_text.append(
            "A modern CLI toolkit for scaffolding FastAPI projects with production-ready\n", style="white")
        welcome_text.append(
            "templates, integrations, and best practices.\n", style="white")

        console.print(Align.center(welcome_text))
        console.print()

        # Display features
        console.print(create_feature_showcase())
        console.print()

        # Display quick start
        console.print(create_quick_start_panel())
        console.print()

        # Display info links
        console.print(create_info_section())
        console.print()

        # Simple footer
        console.print(Align.center(
            "[dim]Use 'fastkit --help' for detailed command information[/dim]"))
        console.print()


# Register commands with better help descriptions
app.command(
    name="greet",
    help="🎉 Greet someone with style (demo command)"
)(greet)

app.command(
    name="version",
    help="📋 Show FastKit version and system information"
)(version)

app.command(
    name="create-project",
    help="🏗️  Create a new FastAPI project with architecture, database, cache, and auth options"
)(create_project)

app.command(
    name="add-domain",
    help="🏢 Add a business domain (users, products, orders) with models, services, and routes"
)(add_domain)

app.command(
    name="add-service",
    help="🔧 Add services to existing project: DB | CACHE | AUTH | JOBS"
)(add_service)

@app.command(name="services", help="📖 Show comprehensive service guide with comparisons")
def services_guide():
    """Display the comprehensive service guide."""
    display_service_help()


@app.command(name="domains", help="📖 Show comprehensive domain guide with examples")
def domains_guide():
    """Display the comprehensive domain guide."""
    display_domain_help()
