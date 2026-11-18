# Nodes

All the nodes are in the **USD** section of the palette. They go inside a **Remote Client**
node, see [Using the nodes](../graphs.md).

| Page | Nodes | Tags |
| --- | --- | --- |
| [Stages](stages.md) | Open, create, save and close a stage. | `stage` |
| [Prims](prims.md) | Add, remove, rename, move, copy, find and query prims, kind, active, metadata. | `prim`, `metadata` |
| [Attributes](attributes.md) | Set and get attributes, over time, list, remove. | `attribute`, `time` |
| [Stage settings](stage-settings.md) | Metadata, time range, fps, up axis, units, default prim, stage info. | `stage`, `settings`, `time`, `metadata` |
| [Composition](composition.md) | References, payloads, inherits, sublayers, variants, export and flatten. | `composition`, `layers`, `variants`, `export` |
| [Transforms, geometry, shading](geometry.md) | Transforms, bounds, visibility, shapes, meshes, materials. | `transform`, `geometry`, `shading` |

The **USD Client** node is described in [Starting a client](../starting-a-client.md).

## Finding nodes

Every node has tags, shown on its palette item. Type a tag in the search field of the
palette as `tags:prim` and only the nodes with that tag are listed. `tags:usd` lists them
all.

## What every node has

| Part | Meaning |
| --- | --- |
| `flow` | Execution order, like other nodes. |
| The inputs of the table | The arguments of the operation. The `stage` input takes a [stage handle](../graphs.md#stage-handles). |
| `timeout` | Seconds to wait for the client's answer before failing. 30 by default, 0 or less waits forever. |
| `response` | What the operation gives back. |

In the tables, the **Output** is `stage` when the node gives the handle of the stage it
changed (chain it into the next node), `none` when there is nothing to give, and
otherwise the kind of value: `string`, `bool`, `list`, `dict` or `any`. A value after `=`
is the default of an input; inputs without one start empty.
