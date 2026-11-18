from ..usd_node import OperationSpec, Param
from .common import (
    ATTR_PARAM,
    FLOAT,
    LIST,
    OBJECT,
    PRIM_PARAM,
    STAGE_PARAM,
    STRING,
    TYPE_NAME_PARAM,
    VALUE_PARAM,
)


TIME_PARAM = Param("time", FLOAT, 0.0, "Time code.")

SPECS: tuple[OperationSpec, ...] = (
    OperationSpec(
        "set_attribute",
        "Set Attribute",
        "Sets the value of an attribute, creating it when a type is given.",
        (STAGE_PARAM, PRIM_PARAM, ATTR_PARAM, VALUE_PARAM, TYPE_NAME_PARAM),
        STRING,
        ("attribute",),
    ),
    OperationSpec(
        "get_attribute",
        "Get Attribute",
        "Reads the value of an attribute.",
        (STAGE_PARAM, PRIM_PARAM, ATTR_PARAM),
        OBJECT,
        ("attribute",),
    ),
    OperationSpec(
        "set_attribute_at_time",
        "Set Attribute At Time",
        "Sets the value of an attribute at a time, creating it when a type is given.",
        (
            STAGE_PARAM,
            PRIM_PARAM,
            ATTR_PARAM,
            VALUE_PARAM,
            TIME_PARAM,
            TYPE_NAME_PARAM,
        ),
        STRING,
        ("attribute", "time"),
    ),
    OperationSpec(
        "get_attribute_at_time",
        "Get Attribute At Time",
        "Reads the value of an attribute at a time, interpolated between samples.",
        (STAGE_PARAM, PRIM_PARAM, ATTR_PARAM, TIME_PARAM),
        OBJECT,
        ("attribute", "time"),
    ),
    OperationSpec(
        "get_time_samples",
        "Get Time Samples",
        "Lists the times an attribute has a value at.",
        (STAGE_PARAM, PRIM_PARAM, ATTR_PARAM),
        LIST,
        ("attribute", "time"),
    ),
    OperationSpec(
        "list_attributes",
        "List Attributes",
        "Lists the names of the attributes of a prim.",
        (STAGE_PARAM, PRIM_PARAM),
        LIST,
        ("attribute",),
    ),
    OperationSpec(
        "remove_attribute",
        "Remove Attribute",
        "Removes an attribute from the layer the stage edits.",
        (STAGE_PARAM, PRIM_PARAM, ATTR_PARAM),
        STRING,
        ("attribute",),
    ),
)
