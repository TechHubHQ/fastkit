import typer
from rich import box
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from rich.text import Text

from rich.rule import Rule

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
    🚀 FastKit CLI - Lightning Fast FastAPI Development

    A modern, beautiful CLI toolkit for scaffolding FastAPI projects
    with production-ready templates, integrations, and best practices.
    """
    if help:
        # Show enhanced help with modern styling
        console.clear()
        show_loading_animation()
        print_ascii_msg()

        # Create a styled help panel
        help_content = ctx.get_help()
        help_panel = Panel(
            help_content,
            box=box.ROUNDED,
            border_style="bright_blue",
            title="[bold bright_blue]📚 FastKit Help[/bold bright_blue]",
            title_align="center",
            padding=(1, 2)
        )
        console.print(help_panel)

        # Add footer with additional info
        footer_rule = Rule(
            "[bold bright_cyan]For more information, visit: https://github.com/TechHubHQ/fastkit[/bold bright_cyan]",
            style="bright_cyan"
        )
        console.print(footer_rule)
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        # Clear screen for clean presentation
        console.clear()

        # Show brief loading animation
        show_loading_animation()

        # Display the main interface
        print_ascii_msg()

        # Welcome message with modern styling
        welcome_text = Text()
        welcome_text.append("🎉 ", style="bright_yellow")
        welcome_text.append("Welcome to ", style="white")
        welcome_text.append("FastKit", style="bold bright_cyan")
        welcome_text.append("! ", style="white")
        welcome_text.append("⚡", style="bright_yellow")
        welcome_text.append("\n\n", style="white")
        welcome_text.append(
            "Your ultimate FastAPI development companion.\n", style="bright_white")
        welcome_text.append(
            "Build production-ready APIs in minutes, not hours.", style="dim white")

        welcome_panel = Panel(
            Align.center(welcome_text),
            box=box.DOUBLE_EDGE,
            border_style="bright_green",
            padding=(1, 4)
        )
        console.print(welcome_panel)
        console.print()

        # Display feature showcase
        console.print(create_feature_showcase())
        console.print()

        # Display quick start and info panels
        console.print(create_quick_start_panel())
        console.print()

        # Display tips and stats
        console.print(create_info_panels())
        console.print()

        # Footer with call to action
        footer_text = Text()
        footer_text.append("🌟 ", style="bright_yellow")
        footer_text.append(
            "Ready to build something amazing? Start with ", style="white")
        footer_text.append("fastkit create-project", style="bold bright_blue")
        footer_text.append(" 🌟", style="bright_yellow")

        footer_panel = Panel(
            Align.center(footer_text),
            box=box.HEAVY,
            border_style="bright_yellow",
            padding=(0, 2)
        )
        console.print(footer_panel)

        # Final decorative rule
        console.print(Rule(style="bright_cyan"))


# Register commands with enhanced styling
app.command(help="👋 Greet someone with style")(greet)
app.command(help="📋 Show FastKit version information")(version)
