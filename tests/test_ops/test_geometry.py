import pytest
from pxr import UsdGeom, UsdShade

from nyx_usd import ops
from nyx_usd.ops import _common


def test_set_and_get_transform(stage):
    ops.add_prim(stage, "/node")
    ops.set_transform(stage, "/node", [1, 2, 3], [0, 0, 0], [2, 2, 2])
    matrix = ops.get_transform(stage, "/node")
    assert matrix[3] == [1, 2, 3, 1]
    assert matrix[0][0] == 2 and matrix[1][1] == 2 and matrix[2][2] == 2


def test_set_transform_defaults_and_replacing(stage):
    ops.add_prim(stage, "/node")
    ops.set_transform(stage, "/node", [5, 0, 0])
    ops.set_transform(stage, "/node")
    assert ops.get_transform(stage, "/node")[3] == [0, 0, 0, 1]


def test_set_transform_rotation(stage):
    ops.add_prim(stage, "/node")
    ops.set_transform(stage, "/node", rotate=[0, 0, 90])
    matrix = ops.get_transform(stage, "/node")
    assert matrix[0][1] == pytest.approx(1.0)
    assert matrix[1][0] == pytest.approx(-1.0)


def test_set_transform_validates(stage):
    ops.add_prim(stage, "/node")
    with pytest.raises(ValueError, match="needs 3 numbers"):
        ops.set_transform(stage, "/node", [1, 2])
    with pytest.raises(ValueError, match="No prim"):
        ops.set_transform(stage, "/nothing")


def test_world_transform_includes_the_parents(stage):
    ops.add_prim(stage, "/a")
    ops.add_prim(stage, "/a/b")
    ops.set_transform(stage, "/a", [10, 0, 0])
    ops.set_transform(stage, "/a/b", [0, 5, 0])
    assert ops.get_world_transform(stage, "/a/b")[3] == [10, 5, 0, 1]
    assert ops.get_transform(stage, "/a/b")[3] == [0, 5, 0, 1]


def test_bounding_box(stage):
    ops.create_cube(stage, "/cube", 2.0)
    assert ops.get_bounding_box(stage, "/cube") == [[-1, -1, -1], [1, 1, 1]]
    ops.set_transform(stage, "/cube", [10, 0, 0])
    assert ops.get_bounding_box(stage, "/cube") == [[9, -1, -1], [11, 1, 1]]


def test_visibility(stage):
    ops.create_cube(stage, "/cube")
    ops.set_visibility(stage, "/cube", False)
    imageable = UsdGeom.Imageable(_common.get_prim(stage, "/cube"))
    assert imageable.ComputeVisibility() == UsdGeom.Tokens.invisible
    ops.set_visibility(stage, "/cube", True)
    assert imageable.ComputeVisibility() == UsdGeom.Tokens.inherited


def test_visibility_needs_an_imageable_prim(stage):
    ops.add_prim(stage, "/plain", "")
    with pytest.raises(ValueError, match="Imageable"):
        ops.set_visibility(stage, "/plain", False)


def test_purpose(stage):
    ops.create_cube(stage, "/cube")
    ops.set_purpose(stage, "/cube", "guide")
    assert ops.get_attribute(stage, "/cube", "purpose") == "guide"
    with pytest.raises(ValueError, match="purpose has to be"):
        ops.set_purpose(stage, "/cube", "nothing")


def test_create_shapes(stage):
    ops.create_cube(stage, "/cube", 4.0)
    ops.create_sphere(stage, "/sphere", 2.5)
    assert ops.get_prim_type(stage, "/cube") == "Cube"
    assert ops.get_attribute(stage, "/cube", "size") == 4.0
    assert ops.get_prim_type(stage, "/sphere") == "Sphere"
    assert ops.get_attribute(stage, "/sphere", "radius") == 2.5


def test_create_mesh(stage):
    points = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    ops.create_mesh(stage, "/quad", points, [4], [0, 1, 2, 3])
    assert ops.get_prim_type(stage, "/quad") == "Mesh"
    assert ops.get_attribute(stage, "/quad", "points") == points
    assert ops.get_attribute(stage, "/quad", "faceVertexCounts") == [4]
    assert ops.get_attribute(stage, "/quad", "faceVertexIndices") == [0, 1, 2, 3]
    assert ops.get_bounding_box(stage, "/quad") == [[0, 0, 0], [1, 1, 0]]


def test_create_mesh_validates(stage):
    points = [[0, 0, 0], [1, 0, 0], [1, 1, 0]]
    with pytest.raises(ValueError, match="corners"):
        ops.create_mesh(stage, "/m", points, [4], [0, 1, 2])
    with pytest.raises(ValueError, match="outside"):
        ops.create_mesh(stage, "/m", points, [3], [0, 1, 3])
    with pytest.raises(ValueError, match="needs 3 numbers"):
        ops.create_mesh(stage, "/m", [[0, 0]], [3], [0, 0, 0])


def test_create_and_bind_material(stage):
    ops.create_cube(stage, "/cube")
    ops.create_material(stage, "/mat", [1, 0, 0])
    ops.bind_material(stage, "/cube", "/mat")

    prim = _common.get_prim(stage, "/cube")
    bound, _ = UsdShade.MaterialBindingAPI(prim).ComputeBoundMaterial()
    assert str(bound.GetPath()) == "/mat"
    shader = UsdShade.Shader(_common.get_prim(stage, "/mat/PreviewSurface"))
    assert shader.GetIdAttr().Get() == "UsdPreviewSurface"
    assert tuple(shader.GetInput("diffuseColor").Get()) == (1, 0, 0)
    assert shader.GetOutput("surface")


def test_material_defaults_and_validation(stage):
    ops.create_material(stage, "/mat")
    shader = UsdShade.Shader(_common.get_prim(stage, "/mat/PreviewSurface"))
    assert tuple(shader.GetInput("diffuseColor").Get()) == pytest.approx((0.8,) * 3)
    with pytest.raises(ValueError, match="needs 3 numbers"):
        ops.create_material(stage, "/bad", [1, 0])
    ops.create_cube(stage, "/cube")
    with pytest.raises(ValueError, match="not a Material"):
        ops.bind_material(stage, "/cube", "/cube")
