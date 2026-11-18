# Composition nodes

Tags: `composition`, `layers`, `variants`, `export`

Build a scene out of other files and layers, choose between variants, and get the
result as text or a file.

| Node | Inputs | Output | What it does |
| --- | --- | --- | --- |
| **Add Reference**<br>`usd:add_reference` | `stage`<br>`prim_path` = `"/"`<br>`asset_path`<br>`target_prim` | stage | References a USD file on a prim. |
| **Add Payload**<br>`usd:add_payload` | `stage`<br>`prim_path` = `"/"`<br>`asset_path`<br>`target_prim` | stage | Adds a payload of a USD file to a prim, a reference that can stay unloaded. |
| **Add Inherit**<br>`usd:add_inherit` | `stage`<br>`prim_path` = `"/"`<br>`class_path` | stage | Makes a prim inherit from a class prim. |
| **Add Sublayer**<br>`usd:add_sublayer` | `stage`<br>`layer_path` | stage | Adds a layer file to the sublayers of the root layer. |
| **Remove Sublayer**<br>`usd:remove_sublayer` | `stage`<br>`layer_path` | stage | Removes a layer from the sublayers of the root layer. |
| **List Sublayers**<br>`usd:list_sublayers` | `stage` | list | Lists the sublayers of the root layer. |
| **Add Variant Set**<br>`usd:add_variant_set` | `stage`<br>`prim_path` = `"/"`<br>`set_name`<br>`variants` = `[]` | stage | Adds a variant set with variants to a prim. |
| **Set Variant Selection**<br>`usd:set_variant_selection` | `stage`<br>`prim_path` = `"/"`<br>`set_name`<br>`variant` | stage | Selects a variant of a variant set. |
| **Get Variants**<br>`usd:get_variants` | `stage`<br>`prim_path` = `"/"` | dict | Describes the variant sets of a prim: their variants and selection. |
| **Export To String**<br>`usd:export_to_string` | `stage`<br>`flatten` = `False` | string | Gets the USD text of a stage, optionally flattened into one layer. |
| **Flatten Stage**<br>`usd:flatten_stage` | `stage`<br>`path` | string | Composes a stage into one layer and writes it to a file. |

## Notes

- **Add Reference** and **Add Payload** take a file and, optionally, a `target_prim` in
  it. Without a target, the default prim of that file is used, so a file without one
  gives nothing: set its default prim, or give the target. A payload is a reference that
  can be left unloaded; here it is loaded.
- **Add Inherit** points the prim at a class prim, usually named with a leading
  underscore like `/_class_asset`. It has no effect until that prim exists.
- **Add Sublayer** adds the layer as the weakest of the root layer. **Remove Sublayer**
  takes the path as it was added.
- **Add Variant Set** adds the set and its variants, and keeps variants it already has.
  **Set Variant Selection** with an empty `variant` clears the selection.
  **Get Variants** gives, for every set, its `variants` and its `selection`.
- **Export To String** gives the USDA text of the root layer. With `flatten` the whole
  stage is composed into one layer first, with references, payloads and variants
  resolved. **Flatten Stage** writes that to a file.
