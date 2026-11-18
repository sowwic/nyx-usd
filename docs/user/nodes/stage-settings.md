# Stage setting nodes

Tags: `stage`, `settings`, `time`, `metadata`

Metadata and settings of the stage as a whole: time, axis, units and the default prim.

| Node | Inputs | Output | What it does |
| --- | --- | --- | --- |
| **Set Stage Metadata**<br>`usd:set_stage_metadata` | `stage`<br>`key`<br>`value` | stage | Sets a metadata field of the stage, like comment or documentation. |
| **Get Stage Metadata**<br>`usd:get_stage_metadata` | `stage`<br>`key` | any | Gets a metadata field of the stage. |
| **Set Time Range**<br>`usd:set_time_range` | `stage`<br>`start` = `0.0`<br>`end` = `100.0` | stage | Sets the first and last time code of the stage. |
| **Get Time Range**<br>`usd:get_time_range` | `stage` | list | Gets the first and last time code of the stage. |
| **Set FPS**<br>`usd:set_fps` | `stage`<br>`fps` = `24.0` | stage | Sets the frames per second of the stage. |
| **Set Up Axis**<br>`usd:set_up_axis` | `stage`<br>`axis` = `"Y"` | stage | Sets the up axis of the stage. |
| **Set Meters Per Unit**<br>`usd:set_meters_per_unit` | `stage`<br>`meters` = `1.0` | stage | Sets the size of a unit of the stage in meters, 0.01 for centimeters. |
| **Set Default Prim**<br>`usd:set_default_prim` | `stage`<br>`prim_path` = `"/"` | stage | Sets the prim used when the file is referenced without a target. |
| **Get Stage Info**<br>`usd:get_stage_info` | `stage` | dict | Describes a stage: root layer, default prim, axis, units, time and prim count. |

## Notes

- **Set Up Axis** takes `Y` or `Z`.
- **Set Meters Per Unit** is the size of one unit in meters: `1` for meters, `0.01` for
  centimeters.
- **Set FPS** sets the frames per second and the time codes per second together.
- **Set Time Range** and **Get Time Range** work on the first and last time code. The end
  can't be before the start.
- **Set Default Prim** names the prim that is used when the file is referenced without a
  target prim, see **Add Reference**.
- **Get Stage Info** gives a dictionary with `root_layer`, `default_prim` (empty if there
  is none), `up_axis`, `meters_per_unit`, `fps`, `start`, `end` and `prim_count`.
- **Set Stage Metadata** works on fields like `comment` and `documentation`.
