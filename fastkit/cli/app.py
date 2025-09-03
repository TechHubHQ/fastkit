import typer
from rich.console import Console
from rich.align import Align
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.rule import Rule
from rich import box
from rich.padding import Padding
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

from fastkit.cli.commands.greet import greet
from fastkit.cli.commands.version import version

app = typer.Typer()
console = Console()

# Modern gradient ASCII art with better styling
ascii_msg = Text.from_markup(
    "[bold]" +
    "[rgb(0,255,255)]███████╗[/rgb(0,255,255)][rgb(0,200,255)] █████╗ [/rgb(0,200,255)][rgb(0,150,255)]███████╗[/rgb(0,150,255)][rgb(0,100,255)]████████╗[/rgb(0,100,255)][rgb(100,0,255)]██╗  ██╗[/rgb(100,0,255)][rgb(150,0,255)]██╗[/rgb(150,0,255)][rgb(200,0,255)]████████╗[/rgb(200,0,255)]\n" +
    "[rgb(0,255,200)]██╔════╝[/rgb(0,255,200)][rgb(0,200,200)]██╔══██╗[/rgb(0,200,200)][rgb(0,150,200)]██╔════╝[/rgb(0,150,200)][rgb(0,100,200)]╚══██╔══╝[/rgb(0,100,200)][rgb(100,0,200)]██║ ██╔╝[/rgb(100,0,200)][rgb(150,0,200)]██║[/rgb(150,0,200)][rgb(200,0,200)]╚══██╔══╝[/rgb(200,0,200)]\n" +
    "[rgb(0,255,150)]█████╗  [/rgb(0,255,150)][rgb(0,200,150)]███████║[/rgb(0,200,150)][rgb(0,150,150)]███████╗[/rgb(0,150,150)][rgb(0,100,150)]   ██║   [/rgb(0,100,150)][rgb(100,0,150)]█████╔╝ [/rgb(100,0,150)][rgb(150,0,150)]██║[/rgb(150,0,150)][rgb(200,0,150)]   ██║   [/rgb(200,0,150)]\n" +
    "[rgb(0,255,100)]██╔══╝  [/rgb(0,255,100)][rgb(0,200,100)]██╔══██║[/rgb(0,200,100)][rgb(0,150,100)]╚════██║[/rgb(0,150,100)][rgb(0,100,100)]   ██║   [/rgb(0,100,100)][rgb(100,0,100)]██╔═██╗ [/rgb(100,0,100)][rgb(150,0,100)]██║[/rgb(150,0,100)][rgb(200,0,100)]   ██║   [/rgb(200,0,100)]\n" +
    "[rgb(0,255,50)]██║     [/rgb(0,255,50)][rgb(0,200,50)]██║  ██║[/rgb(0,200,50)][rgb(0,150,50)]███████║[/rgb(0,150,50)][rgb(0,100,50)]   ██║   [/rgb(0,100,50)][rgb(100,0,50)]██║  ██╗[/rgb(100,0,50)][rgb(150,0,50)]██║[/rgb(150,0,50)][rgb(200,0,50)]   ██║   [/rgb(200,0,50)]\n" +
    "[rgb(0,255,0)]╚═╝     [/rgb(0,255,0)][rgb(0,200,0)]╚═╝  ╚═╝[/rgb(0,200,0)][rgb(0,150,0)]╚══════╝[/rgb(0,150,0)][rgb(0,100,0)]   ╚═╝   [/rgb(0,100,0)][rgb(100,0,0)]╚═╝  ╚═╝[/rgb(100,0,0)][rgb(150,0,0)]╚═╝[/rgb(150,0,0)][rgb(200,0,0)]   ╚═╝   [/rgb(200,0,0)]" +
    "[/bold]"
)


def print_ascii_msg():
    """Display the modern gradient ASCII logo with enhanced styling"""
    # Create a beautiful panel for the logo
    logo_panel = Panel(
        Align.center(ascii_msg),
        box=box.DOUBLE_EDGE,
        border_style="bright_cyan",
        padding=(1, 2),
        title="[bold bright_magenta]✨ FastKit CLI ✨[/bold bright_magenta]",
        title_align="center",
        subtitle="[italic dim]Lightning Fast Development[/italic dim]",
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
    quick_start_content.append("Quick Start Commands:\n\n", style="bold bright_white")
    
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
    tips_content.append("• All projects include Docker support\n", style="white")
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
            "[bold bright_cyan]For more information, visit: https://github.com/your-repo/fastkit[/bold bright_cyan]",
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
        welcome_text.append("Your ultimate FastAPI development companion.\n", style="bright_white")
        welcome_text.append("Build production-ready APIs in minutes, not hours.", style="dim white")
        
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
        footer_text.append("Ready to build something amazing? Start with ", style="white")
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
