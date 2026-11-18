"""Transforms, visibility, basic shapes and materials."""

from __future__ import annotations

from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade, Vt

from ._common import get_prim, get_stage, to_json

PURPOSES = ("default", "render", "proxy", "guide")


def _vector(values: list[float], name: str) -> list[float]:
    """Check a list is a vector of three numbers.

    Args:
        values (list[float]): the list.
        name (str): what it is, for the message.

    Raises:
        ValueError: the list doesn't have three numbers.

    Returns:
        list[float]: the values as floats.
    """
    if len(values) != 3:
        raise ValueError(f"{name} needs 3 numbers, not {len(values)}")
    return [float(value) for value in values]


def _xformable(stage: str, prim_path: str) -> UsdGeom.Xformable:
    """Get a prim as transformable.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: no prim at the path, or it has no transform.

    Returns:
        UsdGeom.Xformable: the prim.
    """
    xformable = UsdGeom.Xformable(get_prim(stage, prim_path))
    if not xformable:
        raise ValueError(f"{prim_path} can't be transformed, it is not a Xformable")
    return xformable


def set_transform(
    stage: str,
    prim_path: str,
    translate: list[float] | None = None,
    rotate: list[float] | None = None,
    scale: list[float] | None = None,
) -> str:
    """Set the local transform of a prim, replacing the transform operations it has.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        translate (list[float] | None): x, y and z, `[0, 0, 0]` if omitted.
        rotate (list[float] | None): x, y and z rotation in degrees, `[0, 0, 0]` if
            omitted.
        scale (list[float] | None): x, y and z, `[1, 1, 1]` if omitted.

    Raises:
        ValueError: no prim at the path, it can't be transformed, or a list doesn't
            have three numbers.

    Returns:
        str: handle of the stage.
    """
    translation = _vector([0, 0, 0] if translate is None else translate, "translate")
    rotation = _vector([0, 0, 0] if rotate is None else rotate, "rotate")
    scaling = _vector([1, 1, 1] if scale is None else scale, "scale")
    xformable = _xformable(stage, prim_path)
    xformable.ClearXformOpOrder()
    xformable.AddTranslateOp().Set(Gf.Vec3d(*translation))
    xformable.AddRotateXYZOp().Set(Gf.Vec3f(*rotation))
    xformable.AddScaleOp().Set(Gf.Vec3f(*scaling))
    return stage


def get_transform(stage: str, prim_path: str) -> list[list[float]]:
    """Get the local transform of a prim as a 4x4 matrix.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: no prim at the path, or it can't be transformed.

    Returns:
        list[list[float]]: the matrix, as rows.
    """
    matrix = _xformable(stage, prim_path).GetLocalTransformation(Usd.TimeCode.Default())
    return to_json(matrix)


def get_world_transform(stage: str, prim_path: str) -> list[list[float]]:
    """Get the transform of a prim in the world as a 4x4 matrix.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: no prim at the path, or it can't be transformed.

    Returns:
        list[list[float]]: the matrix, as rows.
    """
    matrix = _xformable(stage, prim_path).ComputeLocalToWorldTransform(
        Usd.TimeCode.Default()
    )
    return to_json(matrix)


def get_bounding_box(stage: str, prim_path: str) -> list[list[float]]:
    """Get the bounds of a prim and what is below it, in the world.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        list[list[float]]: the minimum and maximum corner. Empty bounds have a
            minimum larger than the maximum.
    """
    cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_])
    box = cache.ComputeWorldBound(get_prim(stage, prim_path)).ComputeAlignedRange()
    return [list(box.GetMin()), list(box.GetMax())]


def set_visibility(stage: str, prim_path: str, visible: bool = True) -> str:
    """Show or hide a prim and what is below it.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        visible (bool): whether the prim is visible.

    Raises:
        ValueError: no prim at the path, or it has no visibility.

    Returns:
        str: handle of the stage.
    """
    imageable = UsdGeom.Imageable(get_prim(stage, prim_path))
    if not imageable:
        raise ValueError(f"{prim_path} has no visibility, it is not Imageable")
    if visible:
        imageable.MakeVisible()
    else:
        imageable.MakeInvisible()
    return stage


def set_purpose(stage: str, prim_path: str, purpose: str = "default") -> str:
    """Set the purpose of a prim: what it is drawn for.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        purpose (str): `default`, `render`, `proxy` or `guide`.

    Raises:
        ValueError: no prim at the path, it has no purpose, or the purpose is unknown.

    Returns:
        str: handle of the stage.
    """
    if purpose not in PURPOSES:
        raise ValueError(f"The purpose has to be one of {PURPOSES}, not {purpose!r}")
    imageable = UsdGeom.Imageable(get_prim(stage, prim_path))
    if not imageable:
        raise ValueError(f"{prim_path} has no purpose, it is not Imageable")
    imageable.GetPurposeAttr().Set(purpose)
    return stage


def create_cube(stage: str, prim_path: str, size: float = 1.0) -> str:
    """Define a cube prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        size (float): length of an edge.

    Returns:
        str: handle of the stage.
    """
    UsdGeom.Cube.Define(get_stage(stage), prim_path).GetSizeAttr().Set(float(size))
    return stage


def create_sphere(stage: str, prim_path: str, radius: float = 1.0) -> str:
    """Define a sphere prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        radius (float): radius of the sphere.

    Returns:
        str: handle of the stage.
    """
    UsdGeom.Sphere.Define(get_stage(stage), prim_path).GetRadiusAttr().Set(float(radius))
    return stage


def create_mesh(
    stage: str,
    prim_path: str,
    points: list[list[float]],
    face_vertex_counts: list[int],
    face_vertex_indices: list[int],
) -> str:
    """Define a polygon mesh prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        points (list[list[float]]): position of every vertex, as x, y and z.
        face_vertex_counts (list[int]): number of vertices of every face.
        face_vertex_indices (list[int]): vertex of every corner of every face.

    Raises:
        ValueError: the counts and the indices don't fit, or an index is out of range.

    Returns:
        str: handle of the stage.
    """
    if sum(face_vertex_counts) != len(face_vertex_indices):
        raise ValueError(
            f"The faces have {sum(face_vertex_counts)} corners, "
            f"there are {len(face_vertex_indices)} indices"
        )
    if face_vertex_indices and not 0 <= min(face_vertex_indices) <= max(
        face_vertex_indices
    ) < len(points):
        raise ValueError(f"An index is outside of the {len(points)} points")
    mesh = UsdGeom.Mesh.Define(get_stage(stage), prim_path)
    mesh.GetPointsAttr().Set(
        Vt.Vec3fArray([Gf.Vec3f(*_vector(p, "point")) for p in points])
    )
    mesh.GetFaceVertexCountsAttr().Set(Vt.IntArray([int(c) for c in face_vertex_counts]))
    mesh.GetFaceVertexIndicesAttr().Set(
        Vt.IntArray([int(i) for i in face_vertex_indices])
    )
    return stage


def create_material(
    stage: str, prim_path: str, diffuse_color: list[float] | None = None
) -> str:
    """Define a material with a UsdPreviewSurface shader.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the material. The shader is `PreviewSurface` below it.
        diffuse_color (list[float] | None): red, green and blue, `[0.8, 0.8, 0.8]` if
            omitted.

    Raises:
        ValueError: the color doesn't have three numbers.

    Returns:
        str: handle of the stage.
    """
    color = _vector([0.8, 0.8, 0.8] if diffuse_color is None else diffuse_color, "color")
    usd_stage = get_stage(stage)
    material = UsdShade.Material.Define(usd_stage, prim_path)
    shader = UsdShade.Shader.Define(usd_stage, f"{prim_path}/PreviewSurface")
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*color))
    surface = shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)
    material.CreateSurfaceOutput().ConnectToSource(surface)
    return stage


def bind_material(stage: str, prim_path: str, material_path: str) -> str:
    """Bind a material to a prim and what is below it.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        material_path (str): path of the material prim.

    Raises:
        ValueError: no prim at a path, or `material_path` is not a material.

    Returns:
        str: handle of the stage.
    """
    prim = get_prim(stage, prim_path)
    material = UsdShade.Material(get_prim(stage, material_path))
    if not material:
        raise ValueError(f"{material_path} is not a Material")
    UsdShade.MaterialBindingAPI.Apply(prim).Bind(material)
    return stage
