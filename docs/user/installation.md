# Installation

There are two halves to set up, in two different Pythons:

| Half | Where it runs | What it needs |
| --- | --- | --- |
| The **plugin**: the nodes | Nyx | Nothing to install. Nyx finds it through `NYX_PLUGIN_PATH`. |
| The **operations**: `nyx_usd` | An interpreter with USD | `pxr`, `nyx-bridge` and `nyx_usd`. |

!!! important
    Do not try to `import pxr` in Nyx's own Python. USD is compiled for one Python and
    loading it into another one can crash the process (a segmentation fault). That is why
    the operations run in a separate interpreter.

## Requirements

- [Nyx](https://github.com/sowwic/nyx).
- An interpreter with USD: an OpenUSD build, the `usd-core` package, or the Python of
  Maya, Houdini or Blender. Python 3.11 or newer.
- [uv](https://docs.astral.sh/uv/) (or `pip`) to install the Python packages.

## 1. The plugin for Nyx

The plugin is the `plugins` folder of this repository. Tell Nyx where it is, then start
Nyx:

```sh
NYX_PLUGIN_PATH=/path/to/nyx-usd/plugins nyx
```

`NYX_PLUGIN_PATH` takes several folders, separated by `:` (`;` on Windows). To avoid the
variable, add the folder to the `plugin_paths` value of the Nyx configuration instead.

The nodes are in the **USD** section of the palette. Their icon is the USD logo.

## 2. The operations for the interpreter with USD

In the interpreter that has `pxr`, install `nyx_usd` and `nyx-bridge`:

```sh
uv pip install sowwic-nyx-bridge
uv pip install -e /path/to/nyx-usd      # or: pip install /path/to/nyx-usd
```

`nyx_usd` has no dependencies of its own, it uses the `pxr` the interpreter provides.
Without installing it you can put `/path/to/nyx-usd/src` on that interpreter's
`PYTHONPATH`.

Check it from a shell, using the interpreter you will give to Nyx:

```sh
/path/to/usd/python -c "import pxr, nyx_bridge, nyx_usd; print('ok')"
```

If your USD build needs paths in the environment (`PYTHONPATH`, `PATH`), set them in the
shell Nyx starts from, or in the `env` input of the node that starts the client, see
[Starting a client](starting-a-client.md).

## Maya, Blender and Houdini

These applications ship `pxr`, so their interpreter only needs `nyx_usd` importable (and
the client of that application, see [Starting a client](starting-a-client.md#maya-and-blender)).

!!! note
    In Maya, `pxr` can be imported once the **mayaUsdPlugin** is loaded:
    `cmds.loadPlugin("mayaUsdPlugin")`. Do this before running the nodes.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| The nodes are not in the palette | Nyx was started without `NYX_PLUGIN_PATH`, or it points at the repository root instead of `plugins`. The log lists the plugins it loads. |
| `No module named 'nyx_usd'` on a USD node | `nyx_usd` is not importable in the client's interpreter, see step 2. |
| `No module named 'pxr'` on a USD node | That interpreter has no USD, or its `PYTHONPATH` / `PATH` for the USD build is missing. |
| `No module named 'nyx_bridge'` when the client starts | Install `sowwic-nyx-bridge` in that interpreter. |
| The Nyx process crashes on `import pxr` | `pxr` was imported into Nyx's Python. Only the client's interpreter should have it. |
| `no interpreter, set python or $NYX_USD_PYTHON` | The USD Client node has no interpreter, see [Starting a client](starting-a-client.md). |
| A USD node fails right away, saying it is not inside a Remote Client | Put the node inside a Remote Client node. |
| A Remote Client waits and times out | No client connected. Is the bridge server running in Nyx, and the client started? |
