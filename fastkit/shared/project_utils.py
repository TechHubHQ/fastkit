# fastkit/shared/project_utils.py
from __future__ import annotations

from pathlib import Path


def is_valid_fastkit_project(project_path: Path) -> bool:
    """Return True if the directory is a FastKit project.

    Detection rule:
    - Primary: presence of a unique marker in pyproject.toml under [tool.fastkit].
    - Fallback: return False if pyproject missing or unreadable.
    """
    pyproject = project_path / "pyproject.toml"
    if not pyproject.exists():
        return False
    try:
        content = pyproject.read_text(encoding="utf-8")
        # Simple check to avoid adding a toml dependency in the CLI path.
        return "[tool.fastkit]" in content and "project = true" in content
    except (OSError, UnicodeDecodeError):
        return False
