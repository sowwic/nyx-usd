"""What the operations share: the opened stages and the conversion of values.

Not operations themselves, nodes don't call anything here.
"""

from __future__ import annotations

import typing

from pxr import Gf, Sdf, Usd

STAGES: dict[str, Usd.Stage] = {}
"""Opened stages by handle, the identifier of their root layer."""


def register(stage: Usd.Stage) -> str:
    """Keep a stage open.

    Args:
        stage (Usd.Stage): stage to keep.

    Returns:
        str: handle of the stage, the identifier of its root layer.
    """
    handle = stage.GetRootLayer().identifier
    STAGES[handle] = stage
    return handle


def get_stage(handle: str) -> Usd.Stage:
    """Get an opened stage.

    Args:
        handle (str): handle given by `open_stage` or `create_stage`.

    Raises:
        ValueError: the stage was never opened, or it was closed.

    Returns:
        Usd.Stage: the stage.
    """
    try:
        return STAGES[handle]
    except KeyError:
        raise ValueError(f"Stage is not open: {handle!r}") from None


def get_prim(handle: str, prim_path: str) -> Usd.Prim:
    """Get a prim that has to exist.

    Args:
        handle (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        Usd.Prim: the prim.
    """
    prim = get_stage(handle).GetPrimAtPath(prim_path)
    if not prim:
        raise ValueError(f"No prim at {prim_path!r} in {handle!r}")
    return prim


def get_attribute_of(
    prim: Usd.Prim, attr: str, type_name: str = "", create: bool = False
) -> Usd.Attribute:
    """Get an attribute of a prim, optionally creating it.

    Args:
        prim (Usd.Prim): prim holding the attribute.
        attr (str): attribute name.
        type_name (str): value type like `float` or `float3`, to create a missing
            attribute.
        create (bool): create the attribute if it is missing.

    Raises:
        ValueError: the attribute is missing and can't be created, because `create`
            is off or the type is unknown.

    Returns:
        Usd.Attribute: the attribute.
    """
    attribute = prim.GetAttribute(attr)
    if attribute:
        return attribute
    if not create:
        raise ValueError(f"No attribute {attr!r} on {str(prim.GetPath())!r}")
    value_type = Sdf.ValueTypeNames.Find(type_name)
    if not value_type:
        raise ValueError(
            f"{prim.GetPath()}.{attr} doesn't exist, give a valid type to create it, "
            f"not {type_name!r}"
        )
    return prim.CreateAttribute(attr, value_type)


def to_usd(value: typing.Any, type_name: Sdf.ValueTypeName) -> typing.Any:
    """Convert JSON data to what an attribute of a type takes.

    Args:
        value (Any): JSON value. Lists become vectors, matrices and arrays.
        type_name (Sdf.ValueTypeName): type of the attribute.

    Returns:
        Any: value for `Usd.Attribute.Set`.
    """
    if not isinstance(value, list):
        return value
    python_class = type_name.type.pythonClass
    if type_name.isArray:
        element = type_name.scalarType.type.pythonClass
        if element is not None and value and isinstance(value[0], list):
            value = [element(*each) for each in value]
        return python_class(value) if python_class is not None else value
    return python_class(*value) if python_class is not None else value


def to_json(value: typing.Any) -> typing.Any:
    """Convert a USD value to JSON data.

    Args:
        value (Any): value of an attribute or of metadata.

    Returns:
        Any: JSON value. Vectors, matrices and arrays become lists, dictionaries
            stay dictionaries, what can't be converted its `str`.
    """
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): to_json(each) for key, each in value.items()}
    if isinstance(value, (Gf.Matrix3d, Gf.Matrix4d, Gf.Matrix3f, Gf.Matrix4f)):
        return [list(row) for row in value]
    try:
        return [to_json(each) for each in value]
    except TypeError:
        return str(value)
