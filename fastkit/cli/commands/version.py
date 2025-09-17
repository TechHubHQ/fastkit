import sys
import platform

from rich.console import Console

__version__ = "0.1.0"

console = Console()


def version():
    """Show FastKit version and system information"""

    # Main version display
    console.print()
    console.print(
        f"[bold bright_cyan]FastKit CLI[/bold bright_cyan] [bright_green]v{__version__}[/bright_green]")
    console.print()

    # System information
    console.print("[bold bright_cyan]System Information:[/bold bright_cyan]")
    console.print(f"  Python:       {sys.version.split()[0]}")
    console.print(f"  Platform:     {platform.system()}")
    console.print(f"  Architecture: {platform.machine()}")
    console.print(f"  Build Date:   2024-01-15")
    console.print()

    # Available features
    console.print("[bold bright_cyan]Available Features:[/bold bright_cyan]")
    console.print("  • Project Generator")
    console.print("  • Database Support")
    console.print("  • Service Templates")
    console.print("  • CLI Tools")
    console.print()

    # Links
    console.print("[bold bright_cyan]Links:[/bold bright_cyan]")
    console.print(
        "  Repository: [bright_blue underline]https://github.com/TechHubHQ/fastkit[/bright_blue underline]")
    console.print(
        "  Issues:     [bright_blue underline]https://github.com/TechHubHQ/fastkit/issues[/bright_blue underline]")
    console.print()
