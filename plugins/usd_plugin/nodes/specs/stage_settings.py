from ..usd_node import OperationSpec, Param
from .common import DICT, FLOAT, LIST, OBJECT, PRIM_PARAM, STAGE_PARAM, STRING


SPECS: tuple[OperationSpec, ...] = (
    OperationSpec(
        "set_stage_metadata",
        "Set Stage Metadata",
        "Sets a metadata field of the stage, like comment or documentation.",
        (
            STAGE_PARAM,
            Param("key", STRING, "", "Metadata key."),
            Param("value", OBJECT, None, "Value of the field."),
        ),
        STRING,
        ("stage", "metadata"),
    ),
    OperationSpec(
        "get_stage_metadata",
        "Get Stage Metadata",
        "Gets a metadata field of the stage.",
        (STAGE_PARAM, Param("key", STRING, "", "Metadata key.")),
        OBJECT,
        ("stage", "metadata"),
    ),
    OperationSpec(
        "set_time_range",
        "Set Time Range",
        "Sets the first and last time code of the stage.",
        (
            STAGE_PARAM,
            Param("start", FLOAT, 0.0, "First time code."),
            Param("end", FLOAT, 100.0, "Last time code."),
        ),
        STRING,
        ("stage", "time"),
    ),
    OperationSpec(
        "get_time_range",
        "Get Time Range",
        "Gets the first and last time code of the stage.",
        (STAGE_PARAM,),
        LIST,
        ("stage", "time"),
    ),
    OperationSpec(
        "set_fps",
        "Set FPS",
        "Sets the frames per second of the stage.",
        (STAGE_PARAM, Param("fps", FLOAT, 24.0, "Frames per second.")),
        STRING,
        ("stage", "time"),
    ),
    OperationSpec(
        "set_up_axis",
        "Set Up Axis",
        "Sets the up axis of the stage.",
        (STAGE_PARAM, Param("axis", STRING, "Y", "Y or Z.")),
        STRING,
        ("stage", "settings"),
    ),
    OperationSpec(
        "set_meters_per_unit",
        "Set Meters Per Unit",
        "Sets the size of a unit of the stage in meters, 0.01 for centimeters.",
        (STAGE_PARAM, Param("meters", FLOAT, 1.0, "Meters per unit.")),
        STRING,
        ("stage", "settings"),
    ),
    OperationSpec(
        "set_default_prim",
        "Set Default Prim",
        "Sets the prim used when the file is referenced without a target.",
        (STAGE_PARAM, PRIM_PARAM),
        STRING,
        ("stage", "settings"),
    ),
    OperationSpec(
        "get_stage_info",
        "Get Stage Info",
        "Describes a stage: root layer, default prim, axis, units, time and prim count.",
        (STAGE_PARAM,),
        DICT,
        ("stage", "settings"),
    ),
)
