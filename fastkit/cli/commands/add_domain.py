"""Add domain command for creating new domains in existing projects."""

import os
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console

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

    console.print(
        f"[bold bright_cyan]Adding domain '{domain_name}' to your project[/bold bright_cyan]\n")

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

    # Show summary
    console.print("[bold]Summary[/bold]")
    console.print(f"  Domain:      [cyan]{domain_name}[/cyan]")
    console.print(f"  Project:     [cyan]{project_path}[/cyan]")
    console.print(f"  With tests:  [cyan]{with_tests}[/cyan]")
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

        console.print(
            f"\n[bold bright_green]Domain '{domain_name}' created successfully![/bold bright_green]")
        console.print(
            "[dim]✓ Domain files created[/dim]")
        console.print(
            "[dim]✓ Dependencies synced to pyproject.toml[/dim]")
        console.print(
            f"\nDomain files created in: [underline]{domains_path}[/underline]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print(
            f"1. Edit [cyan]app/domains/{domain_name}/models.py[/cyan] to define your database models")
        console.print(
            f"2. Update [cyan]app/domains/{domain_name}/schemas.py[/cyan] with your API schemas")
        console.print(
            f"3. Implement business logic in [cyan]app/domains/{domain_name}/services.py[/cyan]")
        console.print(
            f"4. The domain routes are automatically available at [cyan]/api/v1/{domain_name}s[/cyan]")

        if with_tests:
            console.print(
                f"5. Run tests with: [cyan]pytest tests/domains/test_{domain_name}/[/cyan]")

    except Exception as e:
        console.print(
            f"\n[bold red]Error creating domain:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


def _is_valid_fastkit_project(project_path: Path) -> bool:
    """Check if the current directory is a valid FastKit project with domain structure."""
    required_paths = [
        project_path / "app",
        project_path / "app" / "domains",
        project_path / "app" / "api",
        project_path / "app" / "core",
        project_path / "app" / "main.py"
    ]

    return all(path.exists() for path in required_paths)


def _is_valid_domain_name(name: str) -> bool:
    """Validate domain name format."""
    import re
    # Allow lowercase letters, numbers, and underscores
    pattern = r'^[a-z][a-z0-9_]*$'
    return bool(re.match(pattern, name)) and len(name) <= 50
