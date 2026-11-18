import pytest

from nyx_usd import ops


def test_stage_metadata(stage):
    ops.set_stage_metadata(stage, "comment", "hello")
    assert ops.get_stage_metadata(stage, "comment") == "hello"
    assert ops.get_stage_metadata(stage, "documentation") in (None, "")


def test_stage_metadata_with_the_wrong_type_raises(stage):
    with pytest.raises(ValueError, match="stage metadata"):
        ops.set_stage_metadata(stage, "comment", 4)


def test_time_range(stage):
    ops.set_time_range(stage, 10, 20)
    assert ops.get_time_range(stage) == [10.0, 20.0]
    with pytest.raises(ValueError, match="before the start"):
        ops.set_time_range(stage, 5, 1)


def test_fps_sets_the_time_codes_per_second_too(stage):
    ops.set_fps(stage, 30)
    info = ops.get_stage_info(stage)
    assert info["fps"] == 30
    assert ops._common.get_stage(stage).GetTimeCodesPerSecond() == 30
    with pytest.raises(ValueError, match="positive"):
        ops.set_fps(stage, 0)


def test_up_axis(stage):
    ops.set_up_axis(stage, "Z")
    assert ops.get_stage_info(stage)["up_axis"] == "Z"
    ops.set_up_axis(stage, "y")
    assert ops.get_stage_info(stage)["up_axis"] == "Y"
    with pytest.raises(ValueError, match="Y or Z"):
        ops.set_up_axis(stage, "X")


def test_meters_per_unit(stage):
    ops.set_meters_per_unit(stage, 0.01)
    assert ops.get_stage_info(stage)["meters_per_unit"] == pytest.approx(0.01)
    with pytest.raises(ValueError, match="positive"):
        ops.set_meters_per_unit(stage, -1)


def test_default_prim(stage):
    assert ops.get_stage_info(stage)["default_prim"] == ""
    ops.add_prim(stage, "/World")
    ops.set_default_prim(stage, "/World")
    assert ops.get_stage_info(stage)["default_prim"] == "/World"
    with pytest.raises(ValueError, match="No prim"):
        ops.set_default_prim(stage, "/nothing")


def test_stage_info(stage):
    ops.add_prim(stage, "/World/a")
    info = ops.get_stage_info(stage)
    assert info["root_layer"] == stage
    assert info["prim_count"] == 2
    assert set(info) == {
        "root_layer",
        "default_prim",
        "up_axis",
        "meters_per_unit",
        "fps",
        "start",
        "end",
        "prim_count",
    }
