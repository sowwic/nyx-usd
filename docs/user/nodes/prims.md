# Prim nodes

Tags: `prim`, `metadata`

Create, query and edit prims: the objects of a stage, found by their path like
`/World/cube`.

| Node | Inputs | Output | What it does |
| --- | --- | --- | --- |
| **Add Prim**<br>`usd:add_prim` | `stage`<br>`prim_path` = `"/"`<br>`type_name` = `"Xform"` | stage | Defines a prim, and the prims above it without a type if they are missing. |
| **Remove Prim**<br>`usd:remove_prim` | `stage`<br>`prim_path` = `"/"` | stage | Removes a prim from the stage. |
| **List Prims**<br>`usd:list_prims` | `stage`<br>`type_name` | list | Lists the prim paths of a stage. |
| **Has Prim**<br>`usd:has_prim` | `stage`<br>`prim_path` = `"/"` | bool | Checks whether a prim exists. |
| **Get Prim Type**<br>`usd:get_prim_type` | `stage`<br>`prim_path` = `"/"` | string | Gets the schema type of a prim. |
| **Get Children**<br>`usd:get_children` | `stage`<br>`prim_path` = `"/"` | list | Lists the paths of the children of a prim. |
| **Get Parent**<br>`usd:get_parent` | `stage`<br>`prim_path` = `"/"` | string | Gets the path of the parent of a prim. |
| **Find Prims**<br>`usd:find_prims` | `stage`<br>`name_pattern`<br>`type_name` | list | Finds the prims whose name matches a regular expression. |
| **Rename Prim**<br>`usd:rename_prim` | `stage`<br>`prim_path` = `"/"`<br>`new_name` | stage | Renames a prim in the layer the stage edits. |
| **Move Prim**<br>`usd:move_prim` | `stage`<br>`prim_path` = `"/"`<br>`new_parent_path` = `"/"` | stage | Moves a prim under another parent in the layer the stage edits. |
| **Copy Prim**<br>`usd:copy_prim` | `stage`<br>`prim_path` = `"/"`<br>`new_path` | stage | Copies a prim and what is below it in the layer the stage edits. |
| **Set Active**<br>`usd:set_active` | `stage`<br>`prim_path` = `"/"`<br>`active` = `True` | stage | Activates or deactivates a prim. Inactive prims are left out of traversals. |
| **Set Kind**<br>`usd:set_kind` | `stage`<br>`prim_path` = `"/"`<br>`kind` = `"component"` | stage | Sets the kind of a prim, like component or assembly. |
| **Set Prim Metadata**<br>`usd:set_prim_metadata` | `stage`<br>`prim_path` = `"/"`<br>`key`<br>`value` | stage | Sets a metadata field of a prim, like documentation or customData. |
| **Get Prim Metadata**<br>`usd:get_prim_metadata` | `stage`<br>`prim_path` = `"/"`<br>`key` | any | Gets a metadata field of a prim. |

## Notes

- **Add Prim** creates the prims above the one you ask for **without a type**. Add a
  parent first, as an `Xform`, if you want to transform it.
- **List Prims** and **Find Prims** skip inactive prims (see **Set Active**) and abstract
  ones, such as classes.
- **Find Prims** takes a regular expression and searches it in the **name** of the prims,
  not in their whole path: `cube_\d+` finds `/a/cube_01` and `/b/cube_02`.
- **Get Parent** gives `/` for a prim at the top.
- **Rename**, **Move** and **Copy Prim** edit the layer the stage edits, the root layer of
  a stage you opened. They fail with the reason from USD if the new name exists or the
  prim only exists through a reference or payload.
- **Set Kind** takes the kinds of USD: `component`, `group`, `assembly`, `subcomponent`.
- **Set Prim Metadata** and **Get Prim Metadata** work on fields like `documentation`,
  `comment` and `customData` (a dictionary). A value of the wrong type for the key fails.
  Some keys have schema defaults, `customData` of a transformable prim includes
  `userDocBrief`.
