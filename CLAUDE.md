# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

nyx-usd runs Pixar USD operations for [Nyx](https://github.com/sowwic/nyx) graphs. Nyx pins Python 3.14 and never imports `pxr`: the USD code runs in a separate interpreter (an OpenUSD build, Maya, Houdini, Blender) that connects to Nyx through `nyx-bridge`. Dependencies are managed with `uv`.

## Commands

The Makefile includes shared targets from `.make/` (fetched from `sowwic/makefiles`; `make update-make` refreshes them).

```sh
uv sync --locked --dev                     # install
make pytest                                # uv run pytest tests
uv run pytest tests/test_ops.py::test_name # single test
make pytest-pdb                            # drop into pdb on failure
make lint | lint-fix | format              # ruff (line length 89, rules E, F, UP)
make check                                 # lint + tests
make mkdocs                                # docs dev server
```

### Tests

- Before writing a test helper or fixture, check `tests/conftest.py` and reuse what is there.
- Coverage (`--cov=nyx_usd`) is always on; the `output_dir` fixture writes under `.test_output/`.

## Architecture

- **`nyx_usd.ops`** holds the USD logic, a package with one module per area (`stages`, `prims`, `attributes`, `stage_settings`, `composition`, `geometry`; `_common` has the opened stages and the JSON conversion). Plain functions that take and return JSON data, import only `pxr` and the standard library, and never import `nyx` or `nyx_bridge`. Stages are identified by their root layer path (a string handle), not by objects. The nodes call `nyx_usd.ops.<name>`, so `__init__.py` imports every operation: add new ones there too.
- There is no USD specific client: the generic `nyx_bridge.client.NyxClient` runs the ops, because the nodes send code importing `nyx_usd.ops`. `nyx_usd` has to be importable in that interpreter. The USD Client node (`nodes/usd_client.py`) is a Launch Process node that builds the command starting the generic client.
- **`plugins/usd_plugin/`** is the Nyx side, found through `NYX_PLUGIN_PATH` (set to `plugins`). It imports only `nyx.api.v1` and the standard library, never `pxr`. Like the Nyx stdlib it has one module per node under `nodes/` and no `__init__.py` files: the plugin loader makes the folder a package, so relative imports work. `nodes/specs/<area>.py` list the nodes (one `OperationSpec` per operation, with tags), `nodes/operations.py` joins them. A spec's inputs must match the signature of its function in `nyx_usd.ops`, same names and order. Tests of the operations are in `tests/test_ops/` and need `pxr` (skipped without it).

## Conventions

- Google-style docstrings (`Args:`, `Returns:`, `Raises:`).
- Prefer flexibility: when a subclass or plugin needs to run code at a point inside a base class's sequence (before or after a step), add an overridable hook (`pre_*` / `post_*`, a no-op in the base class) rather than changing constructor arguments, reordering the subclass `__init__` around `super().__init__`, or copying the base sequence.
- `develop` is the default and PR branch; `main` is the release branch. `VERSION` is the version source (`make update-version` syncs `pyproject.toml`). Record user-visible changes in `CHANGELOG.rst`.

## Docs

- `docs/` is split into `user/` (installing, starting a client, using the nodes, one page of tables per area under `user/nodes/`) and `dev/` (architecture, adding an operation, testing, releasing), listed in `mkdocs.yml`. The API reference is generated from the docstrings.
- The node tables in `docs/user/nodes/` are written by hand: when a spec in `plugins/usd_plugin/nodes/specs/` changes, change its row there too (inputs, defaults, output, description).
- `make mkdocs` serves the docs; `uv run mkdocs build` builds them. The `AutoAPI directory not found` warning comes from the template and is in the sibling repos too.

## Development

- If the current branch is `develop`, ask the user for the GitHub issue number before starting work. Use related branch
- Do not commit unless asked to.
- Do not update CHANGELOG unless asked to
- Do not push extra created worktrees to remote. Once work in them is done - patch it back into feature branch and delete extra worktree created.
- When a task done in a worktree is finished, do this without being asked: exit the worktree (`ExitWorktree` keep), cherry-pick its commit(s) onto the feature branch in the main checkout, then remove the worktree and its branch. Git can't reach the main checkout from inside the worktree session.

## Token hygiene

- Find symbols with the LSP tool if possible before grepping; then Read with offset/limit.
