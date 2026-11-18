from nyx.api.v1 import CoreDatatypes

from ..usd_node import Param


STRING = CoreDatatypes.STRING.value
OBJECT = CoreDatatypes.OBJECT.value
LIST = CoreDatatypes.LIST.value
DICT = CoreDatatypes.DICT.value
BOOL = CoreDatatypes.BOOL.value
FLOAT = CoreDatatypes.FLOAT.value

STAGE_PARAM = Param(
    "stage", STRING, "", "Stage handle (a string) from Open Stage or Create Stage."
)
PRIM_PARAM = Param("prim_path", STRING, "/", "Path of the prim, like /World/cube.")
ATTR_PARAM = Param("attr", STRING, "", "Attribute name.")
TYPE_NAME_PARAM = Param(
    "type_name",
    STRING,
    "",
    "Value type like float or float3, only to create a missing attribute.",
)
VALUE_PARAM = Param("value", OBJECT, None, "Value. A list becomes a vector or an array.")
