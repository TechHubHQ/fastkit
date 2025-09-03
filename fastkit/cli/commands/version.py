import sys
import platform

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich import box
from rich.rule import Rule
from rich.columns import Columns

__version__ = "0.1.0"

console = Console()


def version():
    """📋 Show comprehensive FastKit version and system information"""

    # Main version display
    version_text = Text()
    version_text.append("🚀 ", style="bright_blue")
    version_text.append("FastKit CLI ", style="bold bright_cyan")
    version_text.append("v", style="dim white")
    version_text.append(__version__, style="bold bright_green")
    version_text.append(" 🚀", style="bright_blue")

    version_panel = Panel(
        Align.center(version_text),
        box=box.DOUBLE_EDGE,
        border_style="bright_cyan",
        title="[bold bright_magenta]✨ Version Information ✨[/bold bright_magenta]",
        title_align="center",
        padding=(1, 3)
    )

    # System information table
    system_table = Table(
        show_header=False,
        box=box.ROUNDED,
        border_style="bright_blue",
        title="[bold bright_yellow]💻 System Information[/bold bright_yellow]",
        title_style="bold bright_yellow"
    )

    system_table.add_column("Property", style="bright_cyan", width=15)
    system_table.add_column("Value", style="bright_white", width=25)

    system_table.add_row("🐍 Python", f"{sys.version.split()[0]}")
    system_table.add_row("💻 Platform", platform.system())
    system_table.add_row("🏠 Architecture", platform.machine())
    system_table.add_row("📅 Build Date", "2024-01-15")

    # Features table
    features_table = Table(
        show_header=False,
        box=box.ROUNDED,
        border_style="bright_green",
        title="[bold bright_green]✨ Available Features[/bold bright_green]",
        title_style="bold bright_green"
    )

    features_table.add_column("Feature", style="bright_green", width=20)
    features_table.add_column("Status", style="bright_white", width=15)

    features_table.add_row("🏗️ Project Generator", "[green]✅ Active[/green]")
    features_table.add_row("💾 Database Support", "[green]✅ Active[/green]")
    features_table.add_row("📦 Service Templates", "[green]✅ Active[/green]")
    features_table.add_row("🔧 CLI Tools", "[green]✅ Active[/green]")

    # Dependencies info
    deps_text = Text()
    deps_text.append("📦 Core Dependencies:\n\n", style="bold bright_magenta")
    deps_text.append("• ", style="bright_cyan")
    deps_text.append("FastAPI ", style="white")
    deps_text.append("0.116.1+\n", style="bright_green")
    deps_text.append("• ", style="bright_cyan")
    deps_text.append("Rich ", style="white")
    deps_text.append("14.1.0+\n", style="bright_green")
    deps_text.append("• ", style="bright_cyan")
    deps_text.append("Typer ", style="white")
    deps_text.append("0.17.3+\n", style="bright_green")
    deps_text.append("• ", style="bright_cyan")
    deps_text.append("Halo ", style="white")
    deps_text.append("0.0.31+", style="bright_green")

    deps_panel = Panel(
        deps_text,
        box=box.ROUNDED,
        border_style="bright_magenta",
        title="[bold bright_magenta]📦 Dependencies[/bold bright_magenta]",
        title_align="left",
        padding=(1, 2)
    )

    # Display everything
    console.print()
    console.print(version_panel)
    console.print()

    # Display tables side by side
    console.print(
        Columns([system_table, features_table], equal=True, expand=True))
    console.print()

    console.print(deps_panel)
    console.print()

    # Footer with links
    footer_text = Text()
    footer_text.append("🔗 ", style="bright_blue")
    footer_text.append("GitHub: ", style="white")
    footer_text.append("https://github.com/TechHubHQ/fastkit",
                       style="bright_blue underline")
    footer_text.append("  •  ", style="dim white")
    footer_text.append("📚 ", style="bright_green")
    footer_text.append("Docs: ", style="white")
    footer_text.append("https://fastkit.dev", style="bright_green underline")

    footer_panel = Panel(
        Align.center(footer_text),
        box=box.HEAVY,
        border_style="bright_yellow",
        padding=(0, 2)
    )
    console.print(footer_panel)

    # Final decorative rule
    console.print(Rule(
        "[bright_cyan]Thank you for using FastKit! 🚀[/bright_cyan]", style="bright_cyan"))
    console.print()
