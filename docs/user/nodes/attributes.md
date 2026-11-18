# Attribute nodes

Tags: `attribute`, `time`

Read and write the attributes of a prim, with or without a time.

| Node | Inputs | Output | What it does |
| --- | --- | --- | --- |
| **Set Attribute**<br>`usd:set_attribute` | `stage`<br>`prim_path` = `"/"`<br>`attr`<br>`value`<br>`type_name` | stage | Sets the value of an attribute, creating it when a type is given. |
| **Get Attribute**<br>`usd:get_attribute` | `stage`<br>`prim_path` = `"/"`<br>`attr` | any | Reads the value of an attribute. |
| **Set Attribute At Time**<br>`usd:set_attribute_at_time` | `stage`<br>`prim_path` = `"/"`<br>`attr`<br>`value`<br>`time` = `0.0`<br>`type_name` | stage | Sets the value of an attribute at a time, creating it when a type is given. |
| **Get Attribute At Time**<br>`usd:get_attribute_at_time` | `stage`<br>`prim_path` = `"/"`<br>`attr`<br>`time` = `0.0` | any | Reads the value of an attribute at a time, interpolated between samples. |
| **Get Time Samples**<br>`usd:get_time_samples` | `stage`<br>`prim_path` = `"/"`<br>`attr` | list | Lists the times an attribute has a value at. |
| **List Attributes**<br>`usd:list_attributes` | `stage`<br>`prim_path` = `"/"` | list | Lists the names of the attributes of a prim. |
| **Remove Attribute**<br>`usd:remove_attribute` | `stage`<br>`prim_path` = `"/"`<br>`attr` | stage | Removes an attribute from the layer the stage edits. |

## Notes

- **Set Attribute** sets an existing attribute. To make one, give its `type_name`, the
  USD value type: `float`, `int`, `bool`, `string`, `token`, `float3`, `color3f`,
  `point3f[]`, `int[]` and so on. Without it, a missing attribute is an error.
- A list `value` becomes what the attribute needs: a vector (`[1, 0.5, 0]` for a
  `color3f`), a matrix or an array. Lists of lists make arrays of vectors, like the
  `points` of a mesh.
- **Get Attribute** gives numbers and text as they are, and vectors, matrices and arrays
  as lists. An attribute without a value gives nothing.
- The `time` nodes use time codes, the unit of the stage (frames at the fps of the stage).
  **Get Attribute At Time** interpolates between samples. **Get Time Samples** gives an
  empty list for an attribute that is not animated.
- **List Attributes** includes the attributes the schema of the prim defines, not only
  the ones that have a value.
- **Remove Attribute** removes the attribute from the layer the stage edits.
