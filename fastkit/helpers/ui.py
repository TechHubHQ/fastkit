import time
from rich.progress import track
from halo import Halo
from rich.console import Console

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
