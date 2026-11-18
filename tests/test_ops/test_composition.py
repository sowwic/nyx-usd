import pathlib

import pytest
from pxr import Usd

from nyx_usd import ops
from nyx_usd.ops import _common


@pytest.fixture
def asset(output_dir: pathlib.Path, request) -> str:
    """Path of a saved file with a cube of size 3 at /Thing, with Thing as default."""
    path = output_dir / f"{request.node.name}_asset.usda"
    path.unlink(missing_ok=True)
    handle = ops.create_stage(path.as_posix())
    ops.create_cube(handle, "/Thing", 3.0)
    ops.set_default_prim(handle, "/Thing")
    ops.save_stage(handle)
    ops.close_stage(handle)
    return path.as_posix()


def test_add_reference_with_a_target(stage, asset):
    ops.add_reference(stage, "/ref", asset, "/Thing")
    assert ops.list_prims(stage) == ["/ref"]
    assert ops.get_attribute(stage, "/ref", "size") == 3.0


def test_add_reference_without_target_uses_the_default_prim(stage, asset):
    ops.add_reference(stage, "/ref", asset)
    assert ops.get_attribute(stage, "/ref", "size") == 3.0


def test_add_payload(stage, asset):
    ops.add_payload(stage, "/pay", asset)
    assert ops.get_attribute(stage, "/pay", "size") == 3.0
    ops.add_payload(stage, "/pay2", asset, "/Thing")
    assert ops.get_attribute(stage, "/pay2", "size") == 3.0


def test_add_inherit(stage):
    ops.add_prim(stage, "/_class_cube", "Cube")
    ops.set_attribute(stage, "/_class_cube", "size", 7.0)
    ops.add_prim(stage, "/cube", "Cube")
    ops.add_inherit(stage, "/cube", "/_class_cube")
    assert ops.get_attribute(stage, "/cube", "size") == 7.0


def test_sublayers(stage, asset):
    assert ops.list_sublayers(stage) == []
    ops.add_sublayer(stage, asset)
    assert ops.list_sublayers(stage) == [asset]
    assert ops.get_attribute(stage, "/Thing", "size") == 3.0
    ops.remove_sublayer(stage, asset)
    assert ops.list_sublayers(stage) == []
    assert not ops.has_prim(stage, "/Thing")
    with pytest.raises(ValueError, match="not a sublayer"):
        ops.remove_sublayer(stage, asset)


def test_variants_change_what_the_prim_has(stage):
    # No local size: a local opinion would be stronger than the ones of the variants
    ops.add_prim(stage, "/cube", "Cube")
    ops.add_variant_set(stage, "/cube", "size", ["small", "big"])
    prim = _common.get_prim(stage, "/cube")
    variant_set = prim.GetVariantSet("size")
    for name, value in (("small", 1.0), ("big", 10.0)):
        variant_set.SetVariantSelection(name)
        with variant_set.GetVariantEditContext():
            prim.GetAttribute("size").Set(value)

    ops.set_variant_selection(stage, "/cube", "size", "big")
    assert ops.get_attribute(stage, "/cube", "size") == 10.0
    ops.set_variant_selection(stage, "/cube", "size", "small")
    assert ops.get_attribute(stage, "/cube", "size") == 1.0
    assert ops.get_variants(stage, "/cube") == {
        "size": {"variants": ["big", "small"], "selection": "small"}
    }
    ops.set_variant_selection(stage, "/cube", "size", "")
    assert ops.get_variants(stage, "/cube")["size"]["selection"] == ""


def test_variant_errors(stage):
    ops.add_prim(stage, "/cube")
    with pytest.raises(ValueError, match="no variant set"):
        ops.set_variant_selection(stage, "/cube", "size", "big")
    ops.add_variant_set(stage, "/cube", "size", ["small"])
    with pytest.raises(ValueError, match="no variant"):
        ops.set_variant_selection(stage, "/cube", "size", "big")
    assert ops.get_variants(stage, "/cube") == {
        "size": {"variants": ["small"], "selection": ""}
    }


def test_export_to_string(stage, asset):
    ops.add_reference(stage, "/ref", asset)
    text = ops.export_to_string(stage)
    assert text.startswith("#usda 1.0") and "references" in text
    flat = ops.export_to_string(stage, flatten=True)
    assert "references" not in flat and "size = 3" in flat


def test_flatten_stage(stage, asset, output_dir: pathlib.Path):
    ops.add_reference(stage, "/ref", asset)
    path = output_dir / "flattened.usda"
    path.unlink(missing_ok=True)
    assert ops.flatten_stage(stage, path.as_posix()) == path.as_posix()
    flat = Usd.Stage.Open(path.as_posix())
    assert flat.GetPrimAtPath("/ref").GetAttribute("size").Get() == 3.0
    assert "references" not in path.read_text()
