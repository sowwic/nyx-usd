# Using the nodes

## Stage handles

Opening or creating a stage happens in the client. What the node gives you back is a
**stage handle**: a string that names the opened stage (it is the identifier of its root
layer). Pass it to the `stage` input of every other node that works on that stage.

- **Open Stage** and **Create Stage** output a handle.
- Nodes that **change** a stage (Add Prim, Set Attribute, ...) take a handle and output
  the same handle, so you can chain them: wire the `response` of one to the `stage` of the
  next.
- Nodes that **read** (List Prims, Get Attribute, ...) take a handle and output the
  value. They don't give the handle back, so keep the wire from the node before.
- **Save Stage** writes the stage to its file, or exports it to another file.
- **Close Stage** closes the stage in the client without saving it.

Changes only exist in the client until you save. Closing a stage without saving drops
them.

## Wiring a graph

Every node has a `flow` input and output like other Nyx nodes, a `timeout` (seconds to
wait for the answer, 30 by default, 0 or less waits forever) and a `response` output.

1. Put a **USD Client** node, or a Launch Process node, or nothing if you start the client
   yourself, see [Starting a client](starting-a-client.md).
2. Put a **Remote Client** node inside it.
3. Put the USD nodes inside the Remote Client, chain their `flow`, and wire the
   `response` of the node that gives the stage to the `stage` input of the next ones.

Text inputs are taken as typed: `/World/cube` is the path, no quotes needed. List inputs
take a list, like `[1, 2, 3]`.

If an operation fails, the node fails with the message of the error from the client, for
example `No prim at '/World/cube' in '...'`, `Stage is not open: ...`, or the message of
USD itself.

## Example: build a scene

```text
USD Client
└── Remote Client
    ├── Create Stage       path = /tmp/scene.usda
    ├── Add Prim           prim_path = /World             type_name = Xform
    ├── Create Cube        prim_path = /World/cube        size = 2
    ├── Set Transform      prim_path = /World/cube        translate = [10, 0, 0]
    ├── Set Default Prim   prim_path = /World
    └── Save Stage
```

Wire the `response` of each node into the `stage` of the next one. The file written is:

```usda
#usda 1.0
(
    defaultPrim = "World"
    upAxis = "Y"
)

def Xform "World"
{
    def Cube "cube"
    {
        double size = 2
        float3 xformOp:rotateXYZ = (0, 0, 0)
        float3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (10, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"]
    }
}
```

Add a **Get Bounding Box** node on `/World/cube` and its `response` is
`[[9, -1, -1], [11, 1, 1]]`.

## Example: look into a file

```text
USD Client
└── Remote Client
    ├── Open Stage         path = /path/to/file.usd
    ├── Get Stage Info                      -> response: a dictionary
    ├── List Prims         type_name = Mesh -> response: a list of paths
    └── Get Attribute      prim_path = /World/mesh   attr = points
```

`Get Stage Info` gives `root_layer`, `default_prim`, `up_axis`, `meters_per_unit`, `fps`,
`start`, `end` and `prim_count`. Wire the `response` of **Open Stage** to the `stage` of
each of the nodes that read.

## Things to know

- **Parents have no type.** *Add Prim* with `/World/cube` creates `/World` without a
  type if it is missing, and a prim without a type can't be transformed. Add `/World`
  first, as an `Xform`, then the prims below it.
- **Local values win over variants.** A value set directly on a prim is stronger than the
  value a variant gives, so an attribute you want a variant to control must not be set on
  the prim itself.
- **Rename, Move and Copy Prim** work on the layer the stage edits, the root layer of a
  stage you opened. A prim that only exists through a reference or payload has nothing to
  rename or move there.
- **Values are JSON.** Inputs and outputs are numbers, text, booleans, lists and
  dictionaries. Vectors, matrices and arrays come out as lists, and lists are accepted
  where an attribute needs a vector or an array, for example `[1, 0.5, 0]` for a
  `color3f`.
- **Attributes made on the fly.** *Set Attribute* creates an attribute that is missing
  when you give its `type_name`, such as `float`, `float3`, `color3f`, `token` or
  `string[]`.
- **Find the nodes by tag.** Search the palette for `tags:prim`, `tags:composition` and
  so on, see [Nodes](nodes/index.md).
