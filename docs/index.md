# nyx-usd

USD operations for [Nyx](https://github.com/sowwic/nyx) graphs: open, create, inspect and
edit USD stages with nodes, and save the result. There are nodes for stages, prims,
attributes, metadata and time, composition (references, payloads, sublayers, variants),
transforms, basic geometry and materials.

Nyx itself never imports `pxr`. The USD code runs in **another interpreter** that has USD
(an OpenUSD build, `usd-core`, Maya, Houdini, Blender), which connects to Nyx through
[nyx-bridge](https://github.com/sowwic/nyx-bridge). The nodes send it the work and bring
the result back, so the same graph runs with any of those.

```text
USD Client                                  <- starts the interpreter with USD
└── Remote Client
    └── Create Stage ─▶ Add Prim ─▶ Create Cube ─▶ Set Transform ─▶ Save Stage
```

| If you want to... | Read |
| --- | --- |
| Install the plugin and the Python side, start a client | [User Guide](user/index.md) |
| Look up a node | [Nodes](user/nodes/index.md) |
| Add an operation or work on nyx-usd | [Developer Guide](dev/index.md) |
| Look up a function of `nyx_usd.ops` | API reference (see the navigation) |

Requires Nyx, and an interpreter with USD (`pxr`) and Python 3.11 or newer. See also
[nyx-bridge-maya](https://github.com/sowwic/nyx-bridge-maya) and
[nyx-bridge-blender](https://github.com/sowwic/nyx-bridge-blender) for running the
operations inside those applications.
