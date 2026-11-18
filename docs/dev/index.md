# Developer Guide

This guide is for people who work on nyx-usd itself.

## Setup

```bash
uv sync
make check        # ruff + pytest
make qrc          # compile the Qt resources of the plugin (icons)
make mkdocs       # serve these docs
```

`make help` lists every target. Ruff uses a line length of 89 and the `E`, `F` and `UP`
rules. Docstrings are Google style: the API reference is generated from them.

The tests of the operations need `pxr`, which `usd-core` (a dev dependency) provides, see
[Testing](testing.md).

!!! important
    The two halves of the project must stay apart:

    - `nyx_usd` (the operations) imports **only `pxr` and the standard library**. Never
      `nyx`, `nyx_bridge` or Qt: it has to run in Maya, Blender and a bare USD build.
    - `plugins/usd_plugin` (the nodes) imports **only `nyx.api.v1` and the standard
      library**. Never `pxr`: Nyx runs a Python USD is not built for, and importing it
      there can crash the process.

## Pages

| Page | What you learn |
| --- | --- |
| [Architecture](architecture.md) | The two halves, stage handles, how a node runs an operation, the USD Client node. |
| [Adding an operation](adding-operations.md) | The steps and rules for a new function and node. |
| [Testing](testing.md) | The test layout, the checks that need Nyx, and trying a graph by hand. |
| [Releasing](releasing.md) | Versions, the changelog and `make release`. |
| API reference | Generated from the docstrings (see the navigation). |
