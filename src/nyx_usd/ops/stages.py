"""Opening, creating, saving and closing stages."""

from __future__ import annotations

from pxr import Usd

from ._common import STAGES, get_stage, register


def open_stage(path: str) -> str:
    """Open a USD file.

    Args:
        path (str): file to open.

    Raises:
        ValueError: the file can't be opened.

    Returns:
        str: handle of the stage.
    """
    try:
        stage = Usd.Stage.Open(path)
    except Exception as err:
        raise ValueError(f"Can't open USD file {path!r}: {err}") from err
    return register(stage)


def create_stage(path: str = "") -> str:
    """Create a stage.

    Args:
        path (str): file the stage is saved to. In memory only if empty.

    Returns:
        str: handle of the stage.
    """
    stage = Usd.Stage.CreateNew(path) if path else Usd.Stage.CreateInMemory()
    return register(stage)


def close_stage(stage: str) -> None:
    """Close a stage without saving it. Does nothing if it is not open.

    Args:
        stage (str): stage handle.
    """
    STAGES.pop(stage, None)


def close_all() -> None:
    """Close every opened stage without saving."""
    STAGES.clear()


def save_stage(stage: str, path: str = "") -> str:
    """Save a stage.

    Args:
        stage (str): stage handle.
        path (str): file to export the stage to, its own file if empty.

    Returns:
        str: handle of the stage.
    """
    usd_stage = get_stage(stage)
    if path:
        usd_stage.Export(path)
    else:
        usd_stage.Save()
    return stage
