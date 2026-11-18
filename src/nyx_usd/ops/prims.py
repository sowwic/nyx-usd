"""Querying and editing prims."""

from __future__ import annotations

import re
import typing

from pxr import Sdf, Usd

from ._common import get_prim, get_stage, to_json


def add_prim(stage: str, prim_path: str, type_name: str = "Xform") -> str:
    """Define a prim, creating the prims above it as needed, without a type.

    Define a parent first to give it a type, like `Xform`: an untyped prim can't be
    transformed.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim, like `/World/cube`.
        type_name (str): schema type of the prim, like `Xform` or `Mesh`.

    Returns:
        str: handle of the stage.
    """
    get_stage(stage).DefinePrim(Sdf.Path(prim_path), type_name)
    return stage


def remove_prim(stage: str, prim_path: str) -> str:
    """Remove a prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        str: handle of the stage.
    """
    get_prim(stage, prim_path)
    get_stage(stage).RemovePrim(Sdf.Path(prim_path))
    return stage


def list_prims(stage: str, type_name: str = "") -> list[str]:
    """List the paths of the prims of a stage.

    Args:
        stage (str): stage handle.
        type_name (str): only the prims of this schema type, all if empty.

    Returns:
        list[str]: prim paths.
    """
    return [
        str(prim.GetPath())
        for prim in get_stage(stage).Traverse()
        if not type_name or prim.GetTypeName() == type_name
    ]


def has_prim(stage: str, prim_path: str) -> bool:
    """Check whether a prim exists.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Returns:
        bool: there is a prim at the path.
    """
    return bool(get_stage(stage).GetPrimAtPath(prim_path))


def get_prim_type(stage: str, prim_path: str) -> str:
    """Get the schema type of a prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        str: type name like `Xform`, empty for a prim without a type.
    """
    return str(get_prim(stage, prim_path).GetTypeName())


def get_children(stage: str, prim_path: str) -> list[str]:
    """List the paths of the children of a prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        list[str]: paths of the children.
    """
    return [str(child.GetPath()) for child in get_prim(stage, prim_path).GetChildren()]


def get_parent(stage: str, prim_path: str) -> str:
    """Get the path of the parent of a prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        str: path of the parent, `/` for a prim at the top, empty for the root.
    """
    parent = get_prim(stage, prim_path).GetParent()
    return str(parent.GetPath()) if parent else ""


def find_prims(stage: str, name_pattern: str, type_name: str = "") -> list[str]:
    """Find prims by name.

    Args:
        stage (str): stage handle.
        name_pattern (str): regular expression searched in the name of the prims, not
            their whole path.
        type_name (str): only the prims of this schema type, all if empty.

    Returns:
        list[str]: paths of the prims that match.
    """
    pattern = re.compile(name_pattern)
    return [
        str(prim.GetPath())
        for prim in get_stage(stage).Traverse()
        if pattern.search(prim.GetName())
        and (not type_name or prim.GetTypeName() == type_name)
    ]


def _apply_edit(stage: str, edit: Sdf.NamespaceEdit) -> None:
    """Apply a namespace edit to the layer the stage edits.

    Args:
        stage (str): stage handle.
        edit (Sdf.NamespaceEdit): edit to apply.

    Raises:
        ValueError: the layer can't apply the edit, for instance the prim has no spec
            in it because it only comes from a reference.
    """
    layer = get_stage(stage).GetEditTarget().GetLayer()
    batch = Sdf.BatchNamespaceEdit()
    batch.Add(edit)
    # Python gives a bool when the edit works, and (False, details) when it doesn't
    result = layer.CanApply(batch)
    if isinstance(result, tuple):
        reasons = ", ".join(detail.reason for detail in result[1])
        raise ValueError(f"Can't edit {edit.currentPath}: {reasons}")
    if not result:
        raise ValueError(f"Can't edit {edit.currentPath}")
    layer.Apply(batch)


def rename_prim(stage: str, prim_path: str, new_name: str) -> str:
    """Rename a prim, in the layer the stage edits.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        new_name (str): new name, without the path.

    Raises:
        ValueError: no prim at the path, or the layer can't rename it.

    Returns:
        str: handle of the stage.
    """
    get_prim(stage, prim_path)
    _apply_edit(stage, Sdf.NamespaceEdit.Rename(Sdf.Path(prim_path), new_name))
    return stage


def move_prim(stage: str, prim_path: str, new_parent_path: str) -> str:
    """Move a prim under another parent, in the layer the stage edits.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        new_parent_path (str): path of the new parent, `/` for the top.

    Raises:
        ValueError: no prim at the path, or the layer can't move it.

    Returns:
        str: handle of the stage.
    """
    prim = get_prim(stage, prim_path)
    _apply_edit(
        stage,
        Sdf.NamespaceEdit.ReparentAndRename(
            Sdf.Path(prim_path),
            Sdf.Path(new_parent_path),
            prim.GetName(),
            Sdf.NamespaceEdit.atEnd,
        ),
    )
    return stage


def copy_prim(stage: str, prim_path: str, new_path: str) -> str:
    """Copy a prim with everything below it, in the layer the stage edits.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        new_path (str): path of the copy. The prims above it are created if missing.

    Raises:
        ValueError: no prim at the path, or the layer has no spec to copy.

    Returns:
        str: handle of the stage.
    """
    get_prim(stage, prim_path)
    source, target = Sdf.Path(prim_path), Sdf.Path(new_path)
    layer = get_stage(stage).GetEditTarget().GetLayer()
    if not layer.GetPrimAtPath(source):
        raise ValueError(f"{prim_path} has no spec in {layer.identifier}")
    Sdf.CreatePrimInLayer(layer, target.GetParentPath())
    if not Sdf.CopySpec(layer, source, layer, target):
        raise ValueError(f"Can't copy {prim_path} to {new_path}")
    return stage


def set_active(stage: str, prim_path: str, active: bool = True) -> str:
    """Activate or deactivate a prim. A deactivated prim is left out of traversals.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        active (bool): whether the prim is active.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        str: handle of the stage.
    """
    get_prim(stage, prim_path).SetActive(bool(active))
    return stage


def set_kind(stage: str, prim_path: str, kind: str) -> str:
    """Set the kind of a prim, like `component` or `assembly`.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        kind (str): kind to set.

    Raises:
        ValueError: no prim at the path, or the kind can't be set.

    Returns:
        str: handle of the stage.
    """
    if not Usd.ModelAPI(get_prim(stage, prim_path)).SetKind(kind):
        raise ValueError(f"Can't set kind {kind!r} on {prim_path}")
    return stage


def set_prim_metadata(
    stage: str, prim_path: str, key: str, value: typing.Any = None
) -> str:
    """Set a metadata field of a prim, like `documentation` or `customData`.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        key (str): metadata key.
        value (Any): JSON value.

    Raises:
        ValueError: no prim at the path, or the value doesn't fit the key.

    Returns:
        str: handle of the stage.
    """
    prim = get_prim(stage, prim_path)
    try:
        authored = prim.SetMetadata(key, value)
    except Exception as err:
        raise ValueError(f"Can't set metadata {key!r} of {prim_path}: {err}") from err
    if not authored:
        raise ValueError(f"Can't set metadata {key!r} of {prim_path} to {value!r}")
    return stage


def get_prim_metadata(stage: str, prim_path: str, key: str) -> typing.Any:
    """Get a metadata field of a prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        key (str): metadata key.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        Any: JSON value, None if the field is not set.
    """
    return to_json(get_prim(stage, prim_path).GetMetadata(key))
