import time
from rich.progress import track
from halo import Halo
from rich.align import Align
from rich.text import Text
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
    """Display the clean and elegant ASCII logo"""
    # Get the ASCII art from the assets module
    ascii_msg = get_fastkit_logo()

    console.print()
    console.print(Align.center(ascii_msg))
    console.print(Align.center(
        "[bold bright_cyan]Lightning Fast FastAPI Development[/bold bright_cyan]"))
    console.print()


def create_feature_showcase():
    """Create a clean feature overview"""
    features_text = Text()
    features_text.append("Features:\n", style="bold bright_cyan")
    features_text.append(
        "  • Project scaffolding with modern FastAPI templates\n", style="white")
    features_text.append(
        "  • Database integration (PostgreSQL, SQLite, MongoDB)\n", style="white")
    features_text.append(
        "  • Redis caching with async support\n", style="white")
    features_text.append(
        "  • Docker and CI/CD configurations\n", style="white")
    features_text.append(
        "  • Production-ready microservice patterns\n", style="white")

    return features_text


def create_quick_start_panel():
    """Create a clean quick start guide"""
    quick_start_content = Text()
    quick_start_content.append("Quick Start:\n", style="bold bright_green")
    quick_start_content.append(
        "  fastkit create-project    ", style="bold bright_blue")
    quick_start_content.append(
        "# Create a new FastAPI project\n", style="dim white")
    quick_start_content.append(
        "  fastkit add-domain        ", style="bold bright_blue")
    quick_start_content.append(
        "# Add domain to existing project\n", style="dim white")
    quick_start_content.append(
        "  fastkit add-service       ", style="bold bright_blue")
    quick_start_content.append(
        "# Add service (db/cache/auth) to project\n", style="dim white")
    quick_start_content.append(
        "  fastkit --help            ", style="bold bright_blue")
    quick_start_content.append(
        "# Show all available commands\n", style="dim white")

    return quick_start_content


def create_info_section():
    """Create a clean information section"""
    info_text = Text()
    info_text.append("Documentation: ", style="white")
    info_text.append("https://github.com/TechHubHQ/fastkit\n",
                     style="bright_blue underline")
    info_text.append("Issues & Support: ", style="white")
    info_text.append(
        "https://github.com/TechHubHQ/fastkit/issues\n", style="bright_blue underline")

    return info_text


def show_loading_animation(message: str = "Initializing FastKit..."):
    """Show a brief loading animation with dynamic message"""
    with Progress(
        SpinnerColumn("dots", style="bright_cyan"),
        TextColumn(f"[bright_white]{message}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("loading", total=100)
        for i in range(100):
            time.sleep(0.01)  # Very brief animation
            progress.update(task, advance=1)
