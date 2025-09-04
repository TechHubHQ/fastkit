import typer
from rich.console import Console
from rich.align import Align
from rich.text import Text

from fastkit.shared.ui import *
from fastkit.cli.commands.greet import greet
from fastkit.cli.commands.version import version

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    help: bool = typer.Option(
        None,
        "--help",
        "-h",
        is_eager=True,
        help="Show help for the app or a specific command.",
    ),
):
    """
    FastKit CLI - Lightning Fast FastAPI Development

    A modern CLI toolkit for scaffolding FastAPI projects with production-ready
    templates, integrations, and best practices.
    """
    if help:
        # Show professional help
        console.clear()
        print_ascii_msg()

        # Display help content cleanly
        help_content = ctx.get_help()
        console.print(help_content)
        console.print()

        # Add professional footer with documentation links
        console.print(
            "[bold bright_cyan]Documentation & Support:[/bold bright_cyan]")
        console.print(
            "  Repository: [bright_blue underline]https://github.com/TechHubHQ/fastkit[/bright_blue underline]")
        console.print(
            "  Issues:     [bright_blue underline]https://github.com/TechHubHQ/fastkit/issues[/bright_blue underline]")
        console.print()
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
            "[dim]Use 'fastkit --help' for more information[/dim]"))
        console.print()


# Register commands
app.command(help="Greet someone with style")(greet)
app.command(help="Show FastKit version information")(version)
