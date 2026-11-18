"""Reading and writing attributes, with and without time."""

from __future__ import annotations

import typing

from pxr import Usd

from ._common import get_attribute_of, get_prim, to_json, to_usd


def set_attribute(
    stage: str, prim_path: str, attr: str, value: typing.Any, type_name: str = ""
) -> str:
    """Set the value of an attribute, creating the attribute if it is missing.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        attr (str): attribute name.
        value (Any): JSON value. A list is turned into the vector, matrix or array the
            attribute type calls for.
        type_name (str): value type of the attribute to create, like `float` or
            `float3`. Needed only when the attribute doesn't exist.

    Raises:
        ValueError: no prim at the path, or the attribute is missing and the type
            is unknown.

    Returns:
        str: handle of the stage.
    """
    attribute = get_attribute_of(get_prim(stage, prim_path), attr, type_name, True)
    attribute.Set(to_usd(value, attribute.GetTypeName()))
    return stage


def get_attribute(stage: str, prim_path: str, attr: str) -> typing.Any:
    """Get the value of an attribute.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        attr (str): attribute name.

    Raises:
        ValueError: no prim at the path, or no such attribute.

    Returns:
        Any: JSON value, None if the attribute has no value.
    """
    attribute = get_attribute_of(get_prim(stage, prim_path), attr)
    return to_json(attribute.Get())


def set_attribute_at_time(
    stage: str,
    prim_path: str,
    attr: str,
    value: typing.Any,
    time: float = 0.0,
    type_name: str = "",
) -> str:
    """Set the value of an attribute at a time, creating the attribute if it is missing.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        attr (str): attribute name.
        value (Any): JSON value, see `set_attribute`.
        time (float): time code the value is for.
        type_name (str): value type of the attribute to create, see `set_attribute`.

    Raises:
        ValueError: no prim at the path, or the attribute is missing and the type
            is unknown.

    Returns:
        str: handle of the stage.
    """
    attribute = get_attribute_of(get_prim(stage, prim_path), attr, type_name, True)
    attribute.Set(to_usd(value, attribute.GetTypeName()), Usd.TimeCode(time))
    return stage


def get_attribute_at_time(
    stage: str, prim_path: str, attr: str, time: float = 0.0
) -> typing.Any:
    """Get the value of an attribute at a time, interpolated between samples.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        attr (str): attribute name.
        time (float): time code to read.

    Raises:
        ValueError: no prim at the path, or no such attribute.

    Returns:
        Any: JSON value, None if the attribute has no value.
    """
    attribute = get_attribute_of(get_prim(stage, prim_path), attr)
    return to_json(attribute.Get(Usd.TimeCode(time)))


def get_time_samples(stage: str, prim_path: str, attr: str) -> list[float]:
    """List the times an attribute has a value at.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        attr (str): attribute name.

    Raises:
        ValueError: no prim at the path, or no such attribute.

    Returns:
        list[float]: time codes, empty for an attribute without animation.
    """
    return list(get_attribute_of(get_prim(stage, prim_path), attr).GetTimeSamples())


def list_attributes(stage: str, prim_path: str) -> list[str]:
    """List the names of the attributes of a prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        list[str]: attribute names, the ones of its schema included.
    """
    return [
        attribute.GetName() for attribute in get_prim(stage, prim_path).GetAttributes()
    ]


def remove_attribute(stage: str, prim_path: str, attr: str) -> str:
    """Remove an attribute from the layer the stage edits.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        attr (str): attribute name.

    Raises:
        ValueError: no prim at the path, or the attribute can't be removed.

    Returns:
        str: handle of the stage.
    """
    if not get_prim(stage, prim_path).RemoveProperty(attr):
        raise ValueError(f"Can't remove attribute {attr!r} of {prim_path}")
    return stage
