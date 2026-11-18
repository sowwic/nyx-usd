import pytest

from nyx_usd import ops


def test_set_existing_attribute(stage):
    ops.add_prim(stage, "/cube", "Cube")
    ops.set_attribute(stage, "/cube", "size", 4.0)
    assert ops.get_attribute(stage, "/cube", "size") == 4.0


def test_set_attribute_creates_it_with_a_type(stage):
    ops.add_prim(stage, "/cube", "Cube")
    ops.set_attribute(stage, "/cube", "custom:mass", 2.5, type_name="float")
    assert ops.get_attribute(stage, "/cube", "custom:mass") == 2.5


def test_set_missing_attribute_needs_a_type(stage):
    ops.add_prim(stage, "/cube", "Cube")
    with pytest.raises(ValueError, match="valid type"):
        ops.set_attribute(stage, "/cube", "custom:mass", 2.5)


def test_vector_and_array_attributes_roundtrip(stage):
    ops.add_prim(stage, "/mesh", "Mesh")
    ops.set_attribute(stage, "/mesh", "custom:color", [1, 0.5, 0], type_name="color3f")
    assert ops.get_attribute(stage, "/mesh", "custom:color") == [1, 0.5, 0]
    ops.set_attribute(stage, "/mesh", "faceVertexCounts", [3, 4])
    assert ops.get_attribute(stage, "/mesh", "faceVertexCounts") == [3, 4]
    points = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    ops.set_attribute(stage, "/mesh", "points", points)
    assert ops.get_attribute(stage, "/mesh", "points") == points


def test_get_unknown_attribute_raises(stage):
    ops.add_prim(stage, "/cube", "Cube")
    with pytest.raises(ValueError, match="No attribute"):
        ops.get_attribute(stage, "/cube", "nothing")


def test_attributes_at_time(stage):
    ops.add_prim(stage, "/cube", "Cube")
    ops.set_attribute_at_time(stage, "/cube", "size", 1.0, 0)
    ops.set_attribute_at_time(stage, "/cube", "size", 3.0, 10)
    assert ops.get_time_samples(stage, "/cube", "size") == [0.0, 10.0]
    assert ops.get_attribute_at_time(stage, "/cube", "size", 0) == 1.0
    assert ops.get_attribute_at_time(stage, "/cube", "size", 10) == 3.0
    assert ops.get_attribute_at_time(stage, "/cube", "size", 5) == pytest.approx(2.0)


def test_attribute_at_time_can_create_the_attribute(stage):
    ops.add_prim(stage, "/cube", "Cube")
    ops.set_attribute_at_time(stage, "/cube", "custom:v", 2, 4, type_name="int")
    assert ops.get_time_samples(stage, "/cube", "custom:v") == [4.0]


def test_no_time_samples_without_animation(stage):
    ops.add_prim(stage, "/cube", "Cube")
    ops.set_attribute(stage, "/cube", "size", 2.0)
    assert ops.get_time_samples(stage, "/cube", "size") == []


def test_list_attributes_has_the_ones_of_the_schema_and_custom_ones(stage):
    ops.add_prim(stage, "/cube", "Cube")
    ops.set_attribute(stage, "/cube", "custom:mass", 1.0, type_name="float")
    names = ops.list_attributes(stage, "/cube")
    assert "size" in names and "custom:mass" in names


def test_remove_attribute(stage):
    ops.add_prim(stage, "/cube", "Cube")
    ops.set_attribute(stage, "/cube", "custom:mass", 1.0, type_name="float")
    ops.remove_attribute(stage, "/cube", "custom:mass")
    assert "custom:mass" not in ops.list_attributes(stage, "/cube")
    with pytest.raises(ValueError, match="Can't remove"):
        ops.remove_attribute(stage, "/cube", "custom:mass")
