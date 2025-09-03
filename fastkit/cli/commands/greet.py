from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.rule import Rule
import random

console = Console()

# Fun greeting variations
greetings = [
    ("Hello", "👋", "bright_green"),
    ("Hi there", "🌟", "bright_blue"),
    ("Greetings", "🎉", "bright_magenta"),
    ("Welcome", "🚀", "bright_cyan"),
    ("Hey", "✨", "bright_yellow"),
    ("Howdy", "🤠", "bright_red")
]


def greet(name: str):
    """🎉 Greets the user with a beautifully styled message"""
    # Pick a random greeting style
    greeting_text, emoji, color = random.choice(greetings)

    # Create the main greeting text
    greeting_content = Text()
    greeting_content.append(f"{emoji} ", style="bright_yellow")
    greeting_content.append(f"{greeting_text}, ", style=f"bold {color}")
    greeting_content.append(name, style="bold bright_white")
    greeting_content.append("!", style=f"bold {color}")
    greeting_content.append(f" {emoji}", style="bright_yellow")

    # Add a subtitle
    subtitle_text = Text()
    subtitle_text.append(
        "Hope you're having a fantastic day! 🌈", style="italic dim white")

    # Combine content
    full_content = Text()
    full_content.append_text(greeting_content)
    full_content.append("\n\n")
    full_content.append_text(subtitle_text)

    # Create a beautiful panel
    greeting_panel = Panel(
        Align.center(full_content),
        box=box.ROUNDED,
        border_style=color,
        title=f"[bold {color}]✨ Personal Greeting ✨[/bold {color}]",
        title_align="center",
        padding=(1, 3),
        subtitle="[italic dim]Powered by FastKit CLI[/italic dim]",
        subtitle_align="center"
    )

    console.print()
    console.print(greeting_panel)

    # Add a decorative rule
    console.print(
        Rule(f"[{color}]Have an amazing day![/{color}]", style=color))
    console.print()
