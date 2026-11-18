"""Layers, references, payloads, inherits and variants, and exporting the result."""

from __future__ import annotations

from pxr import Sdf

from ._common import get_prim, get_stage


def add_reference(
    stage: str, prim_path: str, asset_path: str, target_prim: str = ""
) -> str:
    """Reference a USD file on a prim, defining the prim if needed.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        asset_path (str): file to reference.
        target_prim (str): prim of the file to reference, like `/Thing`. Its default
            prim if empty.

    Returns:
        str: handle of the stage.
    """
    prim = get_stage(stage).DefinePrim(Sdf.Path(prim_path))
    if target_prim:
        prim.GetReferences().AddReference(asset_path, Sdf.Path(target_prim))
    else:
        prim.GetReferences().AddReference(asset_path)
    return stage


def add_payload(
    stage: str, prim_path: str, asset_path: str, target_prim: str = ""
) -> str:
    """Add a payload of a USD file to a prim, defining the prim if needed.

    A payload is a reference that can be left unloaded.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        asset_path (str): file to load.
        target_prim (str): prim of the file to load, its default prim if empty.

    Returns:
        str: handle of the stage.
    """
    prim = get_stage(stage).DefinePrim(Sdf.Path(prim_path))
    if target_prim:
        prim.GetPayloads().AddPayload(asset_path, Sdf.Path(target_prim))
    else:
        prim.GetPayloads().AddPayload(asset_path)
    return stage


def add_inherit(stage: str, prim_path: str, class_path: str) -> str:
    """Make a prim inherit from a class prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        class_path (str): path of the class prim, like `/_class_asset`.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        str: handle of the stage.
    """
    get_prim(stage, prim_path).GetInherits().AddInherit(Sdf.Path(class_path))
    return stage


def add_sublayer(stage: str, layer_path: str) -> str:
    """Add a layer file to the sublayers of the root layer, as the weakest one.

    Args:
        stage (str): stage handle.
        layer_path (str): layer file to add.

    Returns:
        str: handle of the stage.
    """
    get_stage(stage).GetRootLayer().subLayerPaths.append(layer_path)
    return stage


def remove_sublayer(stage: str, layer_path: str) -> str:
    """Remove a layer from the sublayers of the root layer.

    Args:
        stage (str): stage handle.
        layer_path (str): layer file to remove, as it was added.

    Raises:
        ValueError: the layer is not a sublayer.

    Returns:
        str: handle of the stage.
    """
    paths = get_stage(stage).GetRootLayer().subLayerPaths
    if layer_path not in paths:
        raise ValueError(f"{layer_path!r} is not a sublayer of {stage!r}")
    paths.remove(layer_path)
    return stage


def list_sublayers(stage: str) -> list[str]:
    """List the sublayers of the root layer, the strongest first.

    Args:
        stage (str): stage handle.

    Returns:
        list[str]: layer paths.
    """
    return list(get_stage(stage).GetRootLayer().subLayerPaths)


def add_variant_set(
    stage: str, prim_path: str, set_name: str, variants: list[str]
) -> str:
    """Add a variant set with variants to a prim. Existing variants are kept.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        set_name (str): name of the variant set.
        variants (list[str]): names of the variants.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        str: handle of the stage.
    """
    variant_set = get_prim(stage, prim_path).GetVariantSets().AddVariantSet(set_name)
    for variant in variants:
        variant_set.AddVariant(variant)
    return stage


def set_variant_selection(
    stage: str, prim_path: str, set_name: str, variant: str
) -> str:
    """Select a variant of a variant set.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        set_name (str): name of the variant set.
        variant (str): variant to select, empty to clear the selection.

    Raises:
        ValueError: no prim at the path, or no such variant set or variant.

    Returns:
        str: handle of the stage.
    """
    prim = get_prim(stage, prim_path)
    if not prim.HasVariantSets() or set_name not in prim.GetVariantSets().GetNames():
        raise ValueError(f"{prim_path} has no variant set {set_name!r}")
    variant_set = prim.GetVariantSet(set_name)
    if variant and variant not in variant_set.GetVariantNames():
        raise ValueError(f"Variant set {set_name!r} has no variant {variant!r}")
    if variant:
        variant_set.SetVariantSelection(variant)
    else:
        variant_set.ClearVariantSelection()
    return stage


def get_variants(stage: str, prim_path: str) -> dict[str, dict]:
    """Describe the variant sets of a prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        dict[str, dict]: by set name, its `variants` and the `selection` (empty if
            none).
    """
    variant_sets = get_prim(stage, prim_path).GetVariantSets()
    return {
        name: {
            "variants": list(variant_sets.GetVariantSet(name).GetVariantNames()),
            "selection": variant_sets.GetVariantSet(name).GetVariantSelection(),
        }
        for name in variant_sets.GetNames()
    }


def export_to_string(stage: str, flatten: bool = False) -> str:
    """Get the USD text of a stage.

    Args:
        stage (str): stage handle.
        flatten (bool): compose everything into one layer first, instead of giving the
            root layer as it is.

    Returns:
        str: USDA text.
    """
    usd_stage = get_stage(stage)
    layer = usd_stage.Flatten() if flatten else usd_stage.GetRootLayer()
    return layer.ExportToString()


def flatten_stage(stage: str, path: str) -> str:
    """Compose a stage into one layer and write it to a file.

    Args:
        stage (str): stage handle.
        path (str): file to write.

    Raises:
        ValueError: the file can't be written.

    Returns:
        str: the path of the file.
    """
    if not get_stage(stage).Flatten().Export(path):
        raise ValueError(f"Can't write {path!r}")
    return path
