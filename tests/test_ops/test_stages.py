import pathlib

import pytest

from nyx_usd import ops


def test_create_and_close_stage(stage):
    assert ops.list_prims(stage) == []
    ops.close_stage(stage)
    with pytest.raises(ValueError, match="not open"):
        ops.list_prims(stage)


def test_close_unknown_stage_is_fine():
    ops.close_stage("nothing")


def test_save_and_open(output_dir: pathlib.Path):
    path = output_dir / "saved.usda"
    path.unlink(missing_ok=True)
    stage = ops.create_stage(path.as_posix())
    ops.add_prim(stage, "/World")
    assert ops.save_stage(stage) == stage
    ops.close_all()

    reopened = ops.open_stage(path.as_posix())
    assert ops.list_prims(reopened) == ["/World"]


def test_save_stage_to_another_file(stage, output_dir: pathlib.Path):
    path = output_dir / "exported.usda"
    path.unlink(missing_ok=True)
    ops.add_prim(stage, "/World")
    ops.save_stage(stage, path.as_posix())
    assert ops.list_prims(ops.open_stage(path.as_posix())) == ["/World"]


def test_open_missing_file_raises(output_dir: pathlib.Path):
    with pytest.raises(ValueError, match="Can't open"):
        ops.open_stage((output_dir / "missing.usda").as_posix())
