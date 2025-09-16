import os
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console

from fastkit.shared.ui import print_ascii_msg, show_loading_animation
from fastkit.generators.project_generator import scaffold_project_structure


console = Console()


def _prompt_with_choices(prompt_text: str, choices: list[str], default: str | None = None) -> str:
    choices_display = "/".join(choices)
    while True:
        value = typer.prompt(
            f"{prompt_text} [{choices_display}]", default=default or choices[0]).strip().lower()
        if value in choices:
            return value
        console.print(
            f"[red]Invalid choice. Please choose one of: {', '.join(choices)}[/red]")


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

    console.print()
    console.print("[bold]Summary[/bold]")
    console.print(f"  Project: [cyan]{project_name}[/cyan]")
    console.print(f"  Auth:    [cyan]{auth_type}[/cyan]")
    console.print(f"  DB:      [cyan]{db_choice}[/cyan]")
    console.print(f"  Cache:   [cyan]{cache_choice}[/cyan]")
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
        auth_type=auth_type,
        db_choice=db_choice,
        cache_choice=cache_choice,
    )

    console.print(
        f"\n[bold bright_green]Project structure created at[/bold bright_green] [underline]{target_dir}[/underline]")
