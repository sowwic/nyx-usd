# Transform, geometry and shading nodes

Tags: `transform`, `geometry`, `shading`

Move prims, make basic shapes and meshes, and give them materials.

| Node | Inputs | Output | What it does |
| --- | --- | --- | --- |
| **Set Transform**<br>`usd:set_transform` | `stage`<br>`prim_path` = `"/"`<br>`translate` = `[0.0, 0.0, 0.0]`<br>`rotate` = `[0.0, 0.0, 0.0]`<br>`scale` = `[1.0, 1.0, 1.0]` | stage | Sets the local transform of a prim, replacing its transform operations. |
| **Get Transform**<br>`usd:get_transform` | `stage`<br>`prim_path` = `"/"` | list | Gets the local transform of a prim as a 4x4 matrix. |
| **Get World Transform**<br>`usd:get_world_transform` | `stage`<br>`prim_path` = `"/"` | list | Gets the transform of a prim in the world as a 4x4 matrix. |
| **Get Bounding Box**<br>`usd:get_bounding_box` | `stage`<br>`prim_path` = `"/"` | list | Gets the bounds of a prim and what is below it, in the world. |
| **Set Visibility**<br>`usd:set_visibility` | `stage`<br>`prim_path` = `"/"`<br>`visible` = `True` | stage | Shows or hides a prim and what is below it. |
| **Set Purpose**<br>`usd:set_purpose` | `stage`<br>`prim_path` = `"/"`<br>`purpose` = `"default"` | stage | Sets what a prim is drawn for: default, render, proxy or guide. |
| **Create Cube**<br>`usd:create_cube` | `stage`<br>`prim_path` = `"/"`<br>`size` = `1.0` | stage | Defines a cube prim. |
| **Create Sphere**<br>`usd:create_sphere` | `stage`<br>`prim_path` = `"/"`<br>`radius` = `1.0` | stage | Defines a sphere prim. |
| **Create Mesh**<br>`usd:create_mesh` | `stage`<br>`prim_path` = `"/"`<br>`points` = `[]`<br>`face_vertex_counts` = `[]`<br>`face_vertex_indices` = `[]` | stage | Defines a polygon mesh prim. |
| **Create Material**<br>`usd:create_material` | `stage`<br>`prim_path` = `"/"`<br>`diffuse_color` = `[0.8, 0.8, 0.8]` | stage | Defines a material with a UsdPreviewSurface shader. |
| **Bind Material**<br>`usd:bind_material` | `stage`<br>`prim_path` = `"/"`<br>`material_path` | stage | Binds a material to a prim and what is below it. |

## Notes

- **Set Transform** replaces the transform operations of the prim with a translate, a
  rotate (X, Y, Z in degrees) and a scale, applied in that order. Only the prims of types
  that can be transformed, like `Xform`, `Cube` and `Mesh`, work.
- **Get Transform** and **Get World Transform** give a 4x4 matrix as a list of rows. The
  translation is the last row: `[10, 0, 0, 1]`. The world transform includes the parents.
- **Get Bounding Box** gives `[[min x, y, z], [max x, y, z]]` of the prim and what is
  below it, in the world. A prim with nothing to measure has a minimum larger than its
  maximum.
- **Set Visibility** needs a prim that is drawable (`Imageable`), **Set Purpose** takes
  `default`, `render`, `proxy` or `guide`.
- **Create Mesh** checks that the counts add up to the indices and that every index is
  one of the points.
- **Create Material** makes a material with a `UsdPreviewSurface` shader named
  `PreviewSurface` below it, with the `diffuse_color` given. **Bind Material** binds a
  material to a prim and what is below it, and fails if the path is not a material.
