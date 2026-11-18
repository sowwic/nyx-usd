import pytest

from nyx_usd import ops


def test_add_and_list_prims(stage):
    ops.add_prim(stage, "/World")
    ops.add_prim(stage, "/World/cube", "Cube")
    assert ops.list_prims(stage) == ["/World", "/World/cube"]
    assert ops.list_prims(stage, "Cube") == ["/World/cube"]


def test_remove_prim(stage):
    ops.add_prim(stage, "/World")
    ops.remove_prim(stage, "/World")
    assert ops.list_prims(stage) == []
    with pytest.raises(ValueError, match="No prim"):
        ops.remove_prim(stage, "/World")


def test_has_prim_and_type(stage):
    ops.add_prim(stage, "/cube", "Cube")
    assert ops.has_prim(stage, "/cube")
    assert not ops.has_prim(stage, "/nothing")
    assert ops.get_prim_type(stage, "/cube") == "Cube"
    with pytest.raises(ValueError, match="No prim"):
        ops.get_prim_type(stage, "/nothing")


def test_children_and_parent(stage):
    ops.add_prim(stage, "/World/a")
    ops.add_prim(stage, "/World/b")
    assert ops.get_children(stage, "/World") == ["/World/a", "/World/b"]
    assert ops.get_parent(stage, "/World/a") == "/World"
    assert ops.get_parent(stage, "/World") == "/"


def test_find_prims_matches_the_name_not_the_path(stage):
    ops.add_prim(stage, "/cubes/cube_01", "Cube")
    ops.add_prim(stage, "/cubes/cube_02", "Cube")
    ops.add_prim(stage, "/cubes/ball", "Sphere")
    assert ops.find_prims(stage, r"cube_\d+") == ["/cubes/cube_01", "/cubes/cube_02"]
    assert ops.find_prims(stage, "cubes") == ["/cubes"]
    assert ops.find_prims(stage, ".", "Sphere") == ["/cubes/ball"]


def test_rename_prim(stage):
    ops.add_prim(stage, "/World/old", "Cube")
    ops.rename_prim(stage, "/World/old", "new")
    assert ops.list_prims(stage) == ["/World", "/World/new"]
    assert ops.get_prim_type(stage, "/World/new") == "Cube"


def test_rename_to_an_existing_name_raises(stage):
    ops.add_prim(stage, "/World/a")
    ops.add_prim(stage, "/World/b")
    with pytest.raises(ValueError, match="Can't edit"):
        ops.rename_prim(stage, "/World/a", "b")


def test_move_prim(stage):
    ops.add_prim(stage, "/a/thing", "Cube")
    ops.add_prim(stage, "/b")
    ops.move_prim(stage, "/a/thing", "/b")
    assert not ops.has_prim(stage, "/a/thing")
    assert ops.get_prim_type(stage, "/b/thing") == "Cube"


def test_copy_prim_with_what_is_below(stage):
    ops.add_prim(stage, "/src/inner", "Cube")
    ops.copy_prim(stage, "/src", "/other/copy")
    assert ops.has_prim(stage, "/src/inner")
    assert ops.get_prim_type(stage, "/other/copy/inner") == "Cube"


def test_copy_prim_without_a_spec_raises(stage, output_dir):
    asset = ops.create_stage((output_dir / "copy_asset.usda").as_posix())
    ops.add_prim(asset, "/Thing/child")
    ops.save_stage(asset)
    ops.add_reference(stage, "/ref", asset, "/Thing")
    # /ref/child only exists through the reference, the layer has no spec for it
    assert ops.has_prim(stage, "/ref/child")
    with pytest.raises(ValueError, match="no spec"):
        ops.copy_prim(stage, "/ref/child", "/copy")


def test_set_active_hides_the_prim_from_traversal(stage):
    ops.add_prim(stage, "/World/a")
    ops.set_active(stage, "/World/a", False)
    assert ops.list_prims(stage) == ["/World"]
    ops.set_active(stage, "/World/a", True)
    assert ops.list_prims(stage) == ["/World", "/World/a"]


def test_set_kind(stage):
    ops.add_prim(stage, "/World")
    ops.set_kind(stage, "/World", "component")
    assert ops.get_prim_metadata(stage, "/World", "kind") == "component"


def test_prim_metadata(stage):
    ops.add_prim(stage, "/World")
    ops.set_prim_metadata(stage, "/World", "documentation", "the world")
    assert ops.get_prim_metadata(stage, "/World", "documentation") == "the world"
    ops.set_prim_metadata(stage, "/World", "customData", {"author": "me", "n": 2})
    # The schema adds entries of its own, like userDocBrief
    custom_data = ops.get_prim_metadata(stage, "/World", "customData")
    assert custom_data["author"] == "me" and custom_data["n"] == 2
    assert ops.get_prim_metadata(stage, "/World", "comment") in (None, "")


def test_prim_metadata_with_the_wrong_type_raises(stage):
    ops.add_prim(stage, "/World")
    with pytest.raises(ValueError, match="Can't set metadata|Invalid value"):
        ops.set_prim_metadata(stage, "/World", "documentation", 4)
