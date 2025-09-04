import random
from rich.console import Console

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
    """Greets the user with a styled message"""
    # Pick a random greeting style
    greeting_text, emoji, color = random.choice(greetings)

    console.print()
    console.print(f"[bold {color}]{greeting_text}, {name}![/bold {color}]")
    console.print("[dim]Hope you're having a great day![/dim]")
    console.print()
