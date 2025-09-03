import time
from rich.progress import track
from halo import Halo
from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


from fastkit.cli.assets.ascii_art import get_fastkit_logo


console = Console()


def progress_demo():
    """Shows a progress bar for a fake task."""
    for step in track(range(10), description="Processing..."):
        time.sleep(0.3)  # simulate work


def loader_demo():
    """Shows a spinner while doing work."""
    spinner = Halo(text='Loading awesome stuff...', spinner='dots')
    spinner.start()
    try:
        time.sleep(3)  # simulate work
        spinner.succeed("Task completed successfully! ✅")
    except Exception:
        spinner.fail("Something went wrong ❌")


def print_ascii_msg():
    """Display the clean and elegant ASCII logo with enhanced styling"""
    # Get the ASCII art from the assets module
    ascii_msg = get_fastkit_logo()

    # Create a beautiful panel for the logo
    logo_panel = Panel(
        Align.center(ascii_msg),
        box=box.ROUNDED,
        border_style="bright_blue",
        padding=(1, 2),
        title="[bold bright_cyan]⚡ FastKit CLI ⚡[/bold bright_cyan]",
        title_align="center",
        subtitle="[italic bright_white]Lightning Fast Development[/italic bright_white]",
        subtitle_align="center"
    )

    console.print()
    console.print(logo_panel)
    console.print()


def create_feature_showcase():
    """Create a modern feature showcase table"""
    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="bright_blue",
        box=box.ROUNDED,
        title="[bold bright_yellow]🚀 FastKit Features[/bold bright_yellow]",
        title_style="bold bright_yellow",
        caption="[italic dim]Build faster, deploy smarter[/italic dim]",
        caption_style="italic dim"
    )

    table.add_column("🎯 Feature", style="bright_green", width=20)
    table.add_column("📝 Description", style="white", width=40)
    table.add_column("⚡ Status", style="bright_magenta", width=12)

    table.add_row(
        "[bold]Project Generator[/bold]",
        "Scaffold FastAPI projects in seconds",
        "[green]✅ Ready[/green]"
    )
    table.add_row(
        "[bold]Database Integration[/bold]",
        "PostgreSQL, SQLite, MongoDB support",
        "[green]✅ Ready[/green]"
    )
    table.add_row(
        "[bold]Caching Layer[/bold]",
        "Redis integration with async support",
        "[green]✅ Ready[/green]"
    )
    table.add_row(
        "[bold]Service Templates[/bold]",
        "Pre-built microservice patterns",
        "[yellow]🔄 Beta[/yellow]"
    )

    return table


def create_quick_start_panel():
    """Create a modern quick start guide"""
    quick_start_content = Text()
    quick_start_content.append("💡 ", style="bright_yellow")
    quick_start_content.append(
        "Quick Start Commands:\n\n", style="bold bright_white")

    commands = [
        ("fastkit --help", "Show all available commands", "🔍"),
        ("fastkit create-project", "Generate a new FastAPI project", "🏗️"),
        ("fastkit add-service", "Add a new service to your project", "⚙️"),
        ("fastkit version", "Check current version", "📋")
    ]

    for cmd, desc, emoji in commands:
        quick_start_content.append(f"{emoji} ", style="bright_cyan")
        quick_start_content.append(f"{cmd}", style="bold bright_blue")
        quick_start_content.append(f"\n   {desc}\n\n", style="dim white")

    return Panel(
        quick_start_content,
        box=box.ROUNDED,
        border_style="bright_green",
        title="[bold bright_green]🚀 Getting Started[/bold bright_green]",
        title_align="left",
        padding=(1, 2)
    )


def create_info_panels():
    """Create informational panels with modern styling"""
    # Tips panel
    tips_content = Text()
    tips_content.append("💡 Pro Tips:\n\n", style="bold bright_yellow")
    tips_content.append("• Use ", style="white")
    tips_content.append("--help", style="bold bright_cyan")
    tips_content.append(" with any command for details\n", style="white")
    tips_content.append(
        "• All projects include Docker support\n", style="white")
    tips_content.append("• Templates are fully customizable\n", style="white")
    tips_content.append("• Built-in testing and CI/CD configs", style="white")

    tips_panel = Panel(
        tips_content,
        box=box.ROUNDED,
        border_style="bright_yellow",
        title="[bold bright_yellow]💡 Tips & Tricks[/bold bright_yellow]",
        title_align="left",
        padding=(1, 2)
    )

    # Stats panel
    stats_content = Text()
    stats_content.append("📊 FastKit Stats:\n\n", style="bold bright_magenta")
    stats_content.append("⚡ ", style="bright_yellow")
    stats_content.append("Setup Time: ", style="white")
    stats_content.append("< 30 seconds\n", style="bold bright_green")
    stats_content.append("🎯 ", style="bright_blue")
    stats_content.append("Code Reduction: ", style="white")
    stats_content.append("80%+\n", style="bold bright_green")
    stats_content.append("🚀 ", style="bright_red")
    stats_content.append("Performance: ", style="white")
    stats_content.append("Production Ready\n", style="bold bright_green")
    stats_content.append("🔧 ", style="bright_cyan")
    stats_content.append("Integrations: ", style="white")
    stats_content.append("15+ Services", style="bold bright_green")

    stats_panel = Panel(
        stats_content,
        box=box.ROUNDED,
        border_style="bright_magenta",
        title="[bold bright_magenta]📊 Performance[/bold bright_magenta]",
        title_align="left",
        padding=(1, 2)
    )

    return Columns([tips_panel, stats_panel], equal=True, expand=True)


def show_loading_animation():
    """Show a brief loading animation for modern feel"""
    with Progress(
        SpinnerColumn("dots", style="bright_cyan"),
        TextColumn("[bright_white]Initializing FastKit..."),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("loading", total=100)
        for i in range(100):
            time.sleep(0.01)  # Very brief animation
            progress.update(task, advance=1)
