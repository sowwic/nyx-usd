# Testing

```bash
make pytest                                              # everything, with coverage
uv run pytest tests/test_ops/test_prims.py::test_rename_prim   # one test
make pytest-pdb                                          # verbose, pdb on failure
make check                                               # lint and tests
```

Coverage (`--cov=nyx_usd`) is on by default. The tests of the operations run against real
USD: `usd-core` is in the `dev` dependency group. Without `pxr` installed, `tests/conftest.py`
leaves `tests/test_ops/` out instead of failing.

## Layout

| File | Covers |
| --- | --- |
| `tests/test_package.py` | The package imports. |
| `tests/test_ops/test_stages.py` | Open, create, save, export and close. |
| `tests/test_ops/test_prims.py` | Add, remove, query, find, rename, move, copy, active, kind, prim metadata. |
| `tests/test_ops/test_attributes.py` | Set and get, creating with a type, vectors and arrays, time samples, list, remove. |
| `tests/test_ops/test_stage_settings.py` | Stage metadata, time range, fps, axis, units, default prim, stage info. |
| `tests/test_ops/test_composition.py` | References, payloads, inherits, sublayers, variants, export and flatten. |
| `tests/test_ops/test_geometry.py` | Transforms, bounds, visibility, purpose, shapes, meshes, materials. |

## Fixtures

- `output_dir` (`tests/conftest.py`): `.test_output/` in the working directory, for files
  the tests write.
- `stage` (`tests/test_ops/conftest.py`): the handle of an empty stage in memory.
- `close_stages` (autouse, same file): closes every stage after each test, so tests don't
  see each other's stages.

## What to cover

- Every operation: the normal result, **and** each `ValueError` it can raise, with
  `pytest.raises(..., match=...)` on a part of the message.
- A write goes through USD again: read it back with another operation, or reopen the
  saved file. Don't only check that nothing failed.
- Values that cross the JSON boundary: vectors, matrices and arrays in both directions.
- Composition tests check the **effect**: that a reference, payload, inherit or variant
  changes what `get_attribute` gives.
- Remember that a value set on a prim directly is stronger than a variant's, so a variant
  test starts from a prim without that value.
- Anything that needs the Python API of USD directly (for example to author inside a
  variant) can use `nyx_usd.ops._common.get_stage(handle)` and `get_prim`.

## Checking the plugin with Nyx

The nodes import Nyx, which is not a dependency of this project, so `pytest` does not
cover them. Check them with the environment of the Nyx repository, with Nyx started
offscreen and the plugin on its path.

```python
# From the Nyx repository: NYX_PLUGIN_PATH=/path/to/nyx-usd/plugins uv run python check.py
import ast, os, pathlib, sys

os.environ["QT_QPA_PLATFORM"] = "offscreen"
from nyx.application import NyxApplication

app = NyxApplication()                      # loads the plugins of NYX_PLUGIN_PATH

signatures = {}
for module in pathlib.Path("/path/to/nyx-usd/src/nyx_usd/ops").glob("*.py"):
    if module.name.startswith("_"):
        continue
    for node in ast.parse(module.read_text()).body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            signatures[node.name] = [arg.arg for arg in node.args.args]

specs = sys.modules["usd_plugin.nyx_plugin.nodes.operations"].OPERATIONS
print([s.name for s in specs if signatures.get(s.name) != [p.name for p in s.params]])
print(set(signatures) - {s.name for s in specs})   # only close_all has no node
```

The first line should print `[]` (no mismatch) and the second `{'close_all'}`. After that:

1. **Create every node** with `create_node(stage, f"usd:{spec.name}")` from `stage_helpers`
   of the Nyx tests. It fails if a spec is invalid.
2. **Run a graph.** Start the bridge server of the app session
   (`app.session.start_bridge_server()`), build `USD Client` (with `python` and
   `env` set to an interpreter with USD and `PYTHONPATH` for `nyx_usd` and `nyx_bridge`)
   with a Remote Client inside, chain a few nodes, and run the stage with
   `stage.crawler.start()`. Read the `response` of the nodes you want to check.

Do it for a change to the plugin side, or to the arguments of a function. A change inside
a function only needs `make check`.

## CI

`.github/workflows/unit_tests.yml` calls the shared Python test workflow (`sowwic/gh-workflows`)
on Python 3.12, and `code_quality.yml` the lint one. Local development uses 3.12 too
(`.python-version`), but the project supports Python 3.11, the Python of Maya 2026: keep
newer syntax out of `nyx_usd`.
