"""
ASCII Art assets for FastKit CLI
Contains the main logo and other ASCII art elements
"""

from rich.text import Text


def get_fastkit_logo():
    """
    Returns the FastKit ASCII logo with blue color only

    Returns:
        Text: Rich Text object containing the styled ASCII art
    """
    ascii_msg = Text.from_markup(
        "[bold blue]███████╗ █████╗ ███████╗████████╗██╗  ██╗██╗████████╗[/bold blue]\n"
        "[bold blue]██╔════╝██╔══██╗██╔════╝╚══██╔══╝██║ ██╔╝██║╚══██╔══╝[/bold blue]\n"
        "[bold blue]█████╗  ███████║███████╗   ██║   █████╔╝ ██║   ██║   [/bold blue]\n"
        "[bold blue]██╔══╝  ██╔══██║╚════██║   ██║   ██╔═██╗ ██║   ██║   [/bold blue]\n"
        "[bold blue]██║     ██║  ██║███████║   ██║   ██║  ██╗██║   ██║   [/bold blue]\n"
        "[bold blue]╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝   ╚═╝   [/bold blue]"
    )
    return ascii_msg


# You can add more ASCII art functions here in the future
def get_loading_spinner():
    """
    Returns a simple ASCII spinner for loading animations

    Returns:
        list: List of spinner frames
    """
    return ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def get_success_icon():
    """
    Returns a success icon

    Returns:
        str: Success icon
    """
    return "✅"


def get_error_icon():
    """
    Returns an error icon

    Returns:
        str: Error icon
    """
    return "❌"


def get_warning_icon():
    """
    Returns a warning icon

    Returns:
        str: Warning icon
    """
    return "⚠️"
