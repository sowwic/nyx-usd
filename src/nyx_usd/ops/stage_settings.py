"""Metadata and settings of a stage: time, axis, units and the default prim."""

from __future__ import annotations

import typing

from pxr import Sdf, UsdGeom

from ._common import get_prim, get_stage, to_json


def set_stage_metadata(stage: str, key: str, value: typing.Any = None) -> str:
    """Set a metadata field of the stage, like `comment` or `documentation`.

    Args:
        stage (str): stage handle.
        key (str): metadata key.
        value (Any): JSON value.

    Raises:
        ValueError: the value doesn't fit the key.

    Returns:
        str: handle of the stage.
    """
    try:
        authored = get_stage(stage).SetMetadata(key, value)
    except Exception as err:
        raise ValueError(f"Can't set stage metadata {key!r}: {err}") from err
    if not authored:
        raise ValueError(f"Can't set stage metadata {key!r} to {value!r}")
    return stage


def get_stage_metadata(stage: str, key: str) -> typing.Any:
    """Get a metadata field of the stage.

    Args:
        stage (str): stage handle.
        key (str): metadata key.

    Returns:
        Any: JSON value, None if the field is not set.
    """
    return to_json(get_stage(stage).GetMetadata(key))


def set_time_range(stage: str, start: float = 0.0, end: float = 100.0) -> str:
    """Set the first and last time code of the stage.

    Args:
        stage (str): stage handle.
        start (float): first time code.
        end (float): last time code.

    Raises:
        ValueError: the end is before the start.

    Returns:
        str: handle of the stage.
    """
    if end < start:
        raise ValueError(f"The end {end} is before the start {start}")
    usd_stage = get_stage(stage)
    usd_stage.SetStartTimeCode(start)
    usd_stage.SetEndTimeCode(end)
    return stage


def get_time_range(stage: str) -> list[float]:
    """Get the first and last time code of the stage.

    Args:
        stage (str): stage handle.

    Returns:
        list[float]: start and end time code.
    """
    usd_stage = get_stage(stage)
    return [usd_stage.GetStartTimeCode(), usd_stage.GetEndTimeCode()]


def set_fps(stage: str, fps: float = 24.0) -> str:
    """Set the frames per second, and the time codes per second with it.

    Args:
        stage (str): stage handle.
        fps (float): frames per second.

    Raises:
        ValueError: the rate is not positive.

    Returns:
        str: handle of the stage.
    """
    if fps <= 0:
        raise ValueError(f"Frames per second have to be positive, not {fps}")
    usd_stage = get_stage(stage)
    usd_stage.SetFramesPerSecond(fps)
    usd_stage.SetTimeCodesPerSecond(fps)
    return stage


def set_up_axis(stage: str, axis: str = "Y") -> str:
    """Set the up axis of the stage.

    Args:
        stage (str): stage handle.
        axis (str): `Y` or `Z`.

    Raises:
        ValueError: the axis is not Y or Z.

    Returns:
        str: handle of the stage.
    """
    tokens = {"Y": UsdGeom.Tokens.y, "Z": UsdGeom.Tokens.z}
    if axis.upper() not in tokens:
        raise ValueError(f"The up axis has to be Y or Z, not {axis!r}")
    UsdGeom.SetStageUpAxis(get_stage(stage), tokens[axis.upper()])
    return stage


def set_meters_per_unit(stage: str, meters: float = 1.0) -> str:
    """Set the size of a unit of the stage in meters, 0.01 for centimeters.

    Args:
        stage (str): stage handle.
        meters (float): meters per unit.

    Raises:
        ValueError: the value is not positive.

    Returns:
        str: handle of the stage.
    """
    if meters <= 0:
        raise ValueError(f"Meters per unit have to be positive, not {meters}")
    UsdGeom.SetStageMetersPerUnit(get_stage(stage), meters)
    return stage


def set_default_prim(stage: str, prim_path: str) -> str:
    """Set the prim that is referenced when the file is referenced without a target.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim, a root prim.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        str: handle of the stage.
    """
    get_stage(stage).SetDefaultPrim(get_prim(stage, prim_path))
    return stage


def get_stage_info(stage: str) -> dict[str, typing.Any]:
    """Describe a stage.

    Args:
        stage (str): stage handle.

    Returns:
        dict[str, Any]: `root_layer`, `default_prim` (empty if there is none),
            `up_axis`, `meters_per_unit`, `fps`, `start`, `end` and `prim_count`.
    """
    usd_stage = get_stage(stage)
    default_prim = usd_stage.GetDefaultPrim()
    root_layer: Sdf.Layer = usd_stage.GetRootLayer()
    return {
        "root_layer": root_layer.identifier,
        "default_prim": str(default_prim.GetPath()) if default_prim else "",
        "up_axis": str(UsdGeom.GetStageUpAxis(usd_stage)),
        "meters_per_unit": UsdGeom.GetStageMetersPerUnit(usd_stage),
        "fps": usd_stage.GetFramesPerSecond(),
        "start": usd_stage.GetStartTimeCode(),
        "end": usd_stage.GetEndTimeCode(),
        "prim_count": len(list(usd_stage.Traverse())),
    }
