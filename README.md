# nyx-usd

![Tests](https://github.com/sowwic/nyx-usd/actions/workflows/unit_tests.yml/badge.svg)
![Code Quality](https://github.com/sowwic/nyx-usd/actions/workflows/code_quality.yml/badge.svg)

USD operations for [Nyx](https://github.com/sowwic/nyx) graphs: stages, prims, attributes,
composition (references, payloads, sublayers, variants), transforms, basic geometry and
materials, as nodes.

Nyx never imports `pxr`. The operations run in an interpreter that has USD (an OpenUSD
build, `usd-core`, Maya, Houdini, Blender) which connects to Nyx through
[nyx-bridge](https://github.com/sowwic/nyx-bridge); the nodes send them to it from inside
a Remote Client node.

## Use

1. In the interpreter with USD, install `nyx-bridge` and this package (`nyx_usd`).
2. Add the `plugins` folder to `NYX_PLUGIN_PATH` and start Nyx. The nodes are in the
   *USD* section of the palette.
3. Put a **USD Client** node in the graph, set its `python` input (or `NYX_USD_PYTHON`),
   a **Remote Client** inside it, and the USD nodes inside that:

   ```text
   USD Client
   └── Remote Client
       └── Create Stage ─▶ Add Prim ─▶ Create Cube ─▶ Set Transform ─▶ Save Stage
   ```

The same graph runs in Maya or Blender with their Nyx client, only the Remote Client
node selecting it changes. Installation, starting a client and every node are in the
[documentation](https://sowwic.github.io/nyx-usd/), or in `docs/`.

## Development

```sh
uv sync            # install the project and dev dependencies
make check         # lint + tests
make qrc           # compile the Qt resources of the plugin
make mkdocs        # serve the docs
make help          # list all targets
```

See the developer guide in the documentation for the architecture and how to add an
operation.

## Releasing

1. Add a `v<version>` entry to `CHANGELOG.rst`, update `VERSION` (`make update-version`) and commit on `main`.
2. `make release VERSION=<version>` tags, pushes (triggering the GitHub release workflow) and back-merges into `develop`.
