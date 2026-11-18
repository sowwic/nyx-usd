# Adding an operation

A new operation is a function, a node spec and tests. Say it is `set_foo` in the area
`prims`.

## 1. The function

In the module of its area (`src/nyx_usd/ops/prims.py`):

```python
def set_foo(stage: str, prim_path: str, foo: float = 1.0) -> str:
    """Set the foo of a prim.

    Args:
        stage (str): stage handle.
        prim_path (str): path of the prim.
        foo (float): the foo.

    Raises:
        ValueError: there is no prim at the path.

    Returns:
        str: handle of the stage.
    """
    prim = get_prim(stage, prim_path)
    ...
    return stage
```

Rules:

- **`stage` comes first**, a handle. Use `get_stage` and `get_prim` from `_common`, they
  raise a clear `ValueError`.
- **JSON in, JSON out.** Arguments are numbers, strings, booleans, lists and
  dictionaries. Return the same, with `to_json` for USD values. Convert lists with
  `to_usd` when an attribute needs a vector or an array.
- **A function that edits returns the handle** (`Returns: str: handle of the stage.`), so
  nodes chain. A function that reads returns the value.
- **Fail with `ValueError`** and a message that names the path or value. Catch the
  exceptions of `pxr` that you can explain, a `Tf` error says little. Check a result
  `False` from `Set...` and `Apply`: USD often reports failure that way.
- **Only `pxr` and the standard library**, and only long-lived USD APIs (`Usd`, `Sdf`,
  `UsdGeom`, `UsdShade`): the same function has to work with the older USD of Maya and
  Houdini.
- **No newer syntax than Python 3.11.** Use `from __future__ import annotations`.
- Docstrings in Google style. They are the API reference.

Then import it in `src/nyx_usd/ops/__init__.py`, in the group of its module **and** in
`__all__`. The nodes call `nyx_usd.ops.set_foo`, so a function that is not there is not
found.

## 2. The node

In the module of the area in `plugins/usd_plugin/nodes/specs/`, add an `OperationSpec` to
`SPECS`:

```python
OperationSpec(
    "set_foo",                  # the function name, also the node type id usd:set_foo
    "Set Foo",                  # shown in the palette
    "Sets the foo of a prim.",  # the description
    (
        STAGE_PARAM,
        PRIM_PARAM,
        Param("foo", FLOAT, 1.0, "The foo."),
    ),
    STRING,                     # datatype of the response
    ("prim",),                  # tags
),
```

- **The params match the function**: the same names, in the same order. A node passes them
  as keyword arguments, a mismatch fails at run time.
- Use `STAGE_PARAM`, `PRIM_PARAM`, `ATTR_PARAM` and the datatypes of `specs/common.py`
  where they fit. The datatype of a stage handle is `STRING`.
- Give a `default` for every input the user would not want to be empty. Lists as
  defaults are copied for each node.
- Tags are what the operation is about (`prim`, `attribute`, `composition`, `transform`,
  `geometry`, `shading`, ...). Reuse the existing ones, they are searchable as
  `tags:prim`.
- A new area is a new module in `specs/` that defines `SPECS`, and a line in
  `nodes/operations.py`.

## 3. Tests

In `tests/test_ops/test_<area>.py`, against real USD. Cover the normal result and each
`ValueError`. The `stage` fixture is an empty stage in memory and stages are closed after
each test. See [Testing](testing.md).

## 4. Check it

```bash
make check
```

Then check the node side with Nyx, see
[Testing](testing.md#checking-the-plugin-with-nyx): the spec matches the signature, the
node can be created, and a graph runs it.

## 5. Document it

- Add a row for the node to the table in `docs/user/nodes/<area>.md`, with the inputs,
  output and description of the spec. The tables are written by hand: keep them in step
  with the specs.
- If the node has a behaviour users trip over, add a line to the notes of that page.
- A user-visible addition goes in `CHANGELOG.rst` when releasing, see
  [Releasing](releasing.md).
