"""Add domain command for creating new domains in existing projects."""

import os
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

from fastkit.shared.ui import print_ascii_msg, show_loading_animation
from fastkit.shared.service_help import display_domain_help, create_domain_examples_panel, create_domain_structure_panel
from fastkit.generators.domain_generator import scaffold_domain
from rich.columns import Columns

console = Console()


def add_domain(
    domain_name: Optional[str] = typer.Argument(
        None,
        help="🏷️  Domain name (e.g., users, products, orders, customers)",
        metavar="DOMAIN_NAME"
    ),
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="📁 Path to the project root (default: current directory)",
        metavar="PATH"
    ),
    with_tests: bool = typer.Option(
        True,
        "--with-tests/--no-tests",
        help="🧪 Create test files for the domain"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="🔄 Overwrite existing domain if it exists"
    ),
    help_flag: bool = typer.Option(
        False,
        "--help",
        "-h",
        help="Show comprehensive domain guide",
        is_eager=True
    )
):
    """
    🏢 Add a business domain with clean architecture patterns.

    Creates a complete domain structure with models, schemas, services,
    repositories, and routes. Each domain follows clean architecture
    principles and integrates automatically with your API.

    🎯 COMMON DOMAINS:
        • users, products, orders, payments, auth, analytics

    📁 GENERATED STRUCTURE:
        • Complete domain files (models, schemas, services, routes)
        • Clean architecture patterns
        • Automatic API integration at /api/v1/{domain}s
        • Optional test files

    📋 QUICK EXAMPLES:
        fastkit add-domain users          # User management domain
        fastkit add-domain products       # Product catalog
        fastkit add-domain orders --no-tests  # Skip test files

    💡 TIP: Run 'fastkit add-domain --help' to see the complete domain guide
         with structure details and more examples.
    """
    # Handle custom help display or missing arguments
    if help_flag or domain_name is None:
        display_domain_help()
        raise typer.Exit()

    console.clear()
    print_ascii_msg()

    # Welcome message
    welcome_text = Text()
    welcome_text.append("🏢 Adding Domain: ", style="bold bright_cyan")
    welcome_text.append(f"'{domain_name}'", style="bold bright_green")
    welcome_text.append(" to your FastAPI project", style="bright_white")

    console.print(Align.center(welcome_text))
    console.print()

    # Show domain info
    domain_info_panel = Panel(
        f"🏢 [bold]Domain Overview:[/bold]\n"
        f"• [cyan]Clean Architecture[/cyan] - Separation of concerns\n"
        f"• [cyan]Auto-generated Files[/cyan] - Models, schemas, services, routes\n"
        f"• [cyan]API Integration[/cyan] - Available at /api/v1/{domain_name}s\n"
        f"• [cyan]Test Coverage[/cyan] - Optional test files included\n"
        f"• [cyan]Database Agnostic[/cyan] - Works with SQL and NoSQL",
        title="[bold bright_green]✨ Domain Features[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )
    console.print(domain_info_panel)
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
            "Make sure you're in a project created with 'fastkit create-project' and it has the domain-based structure.")
        raise typer.Exit(code=1)

    # Validate domain name
    domain_name = domain_name.lower().strip()
    if not _is_valid_domain_name(domain_name):
        console.print(
            f"[bold red]Error:[/bold red] Invalid domain name '{domain_name}'.")
        console.print(
            "Domain names must be lowercase, alphanumeric, and can contain underscores.")
        raise typer.Exit(code=1)

    # Check if domain already exists
    domains_path = project_path / "app" / "domains" / domain_name
    if domains_path.exists() and not force:
        console.print(
            f"[bold yellow]Warning:[/bold yellow] Domain '{domain_name}' already exists.")
        overwrite = typer.confirm(
            "Do you want to overwrite it?", default=False)
        if not overwrite:
            console.print("Aborting.")
            raise typer.Exit(code=1)

    # Beautiful summary with card-style layout
    console.print(
        "[bold bright_cyan]📋 Domain Configuration[/bold bright_cyan]")
    console.print()

    # Create elegant summary content
    summary_content = Text()

    summary_content.append("🏷️  ", style="bright_green")
    summary_content.append("Domain: ", style="bold white")
    summary_content.append(f"{domain_name}", style="bright_green")
    summary_content.append("\n")

    summary_content.append("📁  ", style="bright_blue")
    summary_content.append("Project: ", style="bold white")
    summary_content.append(f"{project_path.name}", style="bright_blue")
    summary_content.append("\n")

    summary_content.append("🧪  ", style="bright_yellow")
    summary_content.append("Tests: ", style="bold white")
    test_status = "Included" if with_tests else "Skipped"
    summary_content.append(
        f"{test_status}", style="bright_yellow" if with_tests else "dim")
    summary_content.append("\n")

    summary_content.append("🔗  ", style="bright_cyan")
    summary_content.append("API Route: ", style="bold white")
    summary_content.append(f"/api/v1/{domain_name}s", style="bright_cyan")
    summary_content.append("\n\n")

    summary_content.append("📝  ", style="bright_magenta")
    summary_content.append("Generated Files: ", style="bold white")
    summary_content.append(
        "models, schemas, services, routes, repositories", style="bright_magenta")

    summary_panel = Panel(
        summary_content,
        title="[bold bright_green]✨ Domain Summary[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )
    console.print(summary_panel)
    console.print()

    proceed = typer.confirm("Proceed to create the domain?", default=True)
    if not proceed:
        console.print("Aborting.")
        raise typer.Exit(code=1)

    show_loading_animation(f"Creating domain '{domain_name}'...")

    # Create the domain
    try:
        scaffold_domain(
            project_path=project_path,
            domain_name=domain_name,
            with_tests=with_tests,
            force=force
        )

        # Success message with next steps
        console.print()
        success_panel = Panel(
            f"🎉 [bold bright_green]Success![/bold bright_green] Domain '{domain_name}' has been created.\n\n"
            f"📁 [bold]Domain Location:[/bold] [cyan]{domains_path}[/cyan]\n\n"
            f"🚀 [bold]Next Steps:[/bold]\n"
            f"  1. [bright_blue]Edit models.py[/bright_blue] - Define your database models\n"
            f"  2. [bright_blue]Update schemas.py[/bright_blue] - Configure API schemas\n"
            f"  3. [bright_blue]Implement services.py[/bright_blue] - Add business logic\n"
            f"  4. [bright_blue]Test your API[/bright_blue] - Available at /api/v1/{domain_name}s\n"
            + (f"  5. [bright_blue]Run tests[/bright_blue] - pytest tests/domains/test_{domain_name}/\n" if with_tests else "") +
            f"\n📚 [bold]Files Created:[/bold]\n"
            f"  • models.py, schemas.py, services.py\n"
            f"  • repositories.py, routes.py, dependencies.py\n"
            f"  • exceptions.py, __init__.py"
            + ("\n  • Complete test suite" if with_tests else ""),
            title="[bold bright_green]✨ Domain Created Successfully![/bold bright_green]",
            border_style="bright_green",
            padding=(1, 2)
        )
        console.print(success_panel)

        # Additional tips
        console.print(
            "[dim]💡 Tip: The domain follows clean architecture patterns with separation of concerns.[/dim]")
        console.print(
            "[dim]💡 Tip: All endpoints include full CRUD operations with proper error handling.[/dim]")
        console.print(
            "\n[bold bright_cyan]Happy domain building! 🏢[/bold bright_cyan]")

    except Exception as e:
        console.print(
            f"\n[bold red]Error creating domain:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


def _is_valid_fastkit_project(project_path: Path) -> bool:
    """Check if the current directory is a valid FastKit project with domain structure."""
    # Prefer the shared detector for consistency
    try:
        from fastkit.shared.project_utils import is_valid_fastkit_project
        return is_valid_fastkit_project(project_path)
    except Exception:
        return False


def _is_valid_domain_name(name: str) -> bool:
    """Validate domain name format."""
    import re
    # Allow lowercase letters, numbers, and underscores
    pattern = r'^[a-z][a-z0-9_]*$'
    return bool(re.match(pattern, name)) and len(name) <= 50
