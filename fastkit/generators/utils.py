"""Shared utility functions for generators."""

from pathlib import Path
from jinja2 import Environment


def ensure_dir(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def render_and_write(template_name: str, dest_path: Path, context: dict, template_env: Environment) -> None:
    """Render template and write to destination file."""
    template = template_env.get_template(template_name)
    content = template.render(context)
    dest_path.write_text(content, encoding='utf-8')
