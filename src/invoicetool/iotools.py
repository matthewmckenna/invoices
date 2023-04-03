from pathlib import Path


def ensure_path(path: Path | str):
    """Ensure that a directory exists, creating if needed"""
    if isinstance(path, str):
        path = Path(path)
    path.expanduser().mkdir(exist_ok=True, parents=True)
    return path
