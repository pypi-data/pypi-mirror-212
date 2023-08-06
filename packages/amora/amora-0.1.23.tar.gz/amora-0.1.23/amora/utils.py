import functools
import sys
from pathlib import Path
from typing import Callable, Iterable, Union

from amora.config import settings


def list_files(path: Union[str, Path], suffix: str) -> Iterable[Path]:
    yield from Path(path).rglob(f"*{suffix}")


def model_path_for_target_path(path: Path) -> Path:
    return Path(
        str(path)
        .replace(settings.target_path.as_posix(), settings.models_path.as_posix())
        .replace(".sql", ".py"),
    )


def target_path_for_model_path(path: Path) -> Path:
    return Path(
        str(path)
        .replace(settings.models_path.as_posix(), settings.target_path.as_posix())
        .replace(".py", ".sql")
    )


def list_target_files() -> Iterable[Path]:
    return list_files(settings.target_path, suffix=".sql")


def ensure_path(func: Callable) -> Callable:
    if settings.models_path not in sys.path:
        sys.path.append(settings.models_path.as_posix())

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
