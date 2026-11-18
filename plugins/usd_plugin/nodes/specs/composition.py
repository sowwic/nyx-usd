from ..usd_node import OperationSpec, Param
from .common import BOOL, DICT, LIST, PRIM_PARAM, STAGE_PARAM, STRING


ASSET_PARAM = Param("asset_path", STRING, "", "File to use.")
TARGET_PARAM = Param(
    "target_prim", STRING, "", "Prim of the file to use, its default if empty."
)
SET_PARAM = Param("set_name", STRING, "", "Name of the variant set.")

SPECS: tuple[OperationSpec, ...] = (
    OperationSpec(
        "add_reference",
        "Add Reference",
        "References a USD file on a prim.",
        (STAGE_PARAM, PRIM_PARAM, ASSET_PARAM, TARGET_PARAM),
        STRING,
        ("composition",),
    ),
    OperationSpec(
        "add_payload",
        "Add Payload",
        "Adds a payload of a USD file to a prim, a reference that can stay unloaded.",
        (STAGE_PARAM, PRIM_PARAM, ASSET_PARAM, TARGET_PARAM),
        STRING,
        ("composition",),
    ),
    OperationSpec(
        "add_inherit",
        "Add Inherit",
        "Makes a prim inherit from a class prim.",
        (
            STAGE_PARAM,
            PRIM_PARAM,
            Param("class_path", STRING, "", "Path of the class prim."),
        ),
        STRING,
        ("composition",),
    ),
    OperationSpec(
        "add_sublayer",
        "Add Sublayer",
        "Adds a layer file to the sublayers of the root layer.",
        (STAGE_PARAM, Param("layer_path", STRING, "", "Layer file.")),
        STRING,
        ("composition", "layers"),
    ),
    OperationSpec(
        "remove_sublayer",
        "Remove Sublayer",
        "Removes a layer from the sublayers of the root layer.",
        (STAGE_PARAM, Param("layer_path", STRING, "", "Layer file, as added.")),
        STRING,
        ("composition", "layers"),
    ),
    OperationSpec(
        "list_sublayers",
        "List Sublayers",
        "Lists the sublayers of the root layer.",
        (STAGE_PARAM,),
        LIST,
        ("composition", "layers"),
    ),
    OperationSpec(
        "add_variant_set",
        "Add Variant Set",
        "Adds a variant set with variants to a prim.",
        (
            STAGE_PARAM,
            PRIM_PARAM,
            SET_PARAM,
            Param("variants", LIST, [], "Names of the variants."),
        ),
        STRING,
        ("composition", "variants"),
    ),
    OperationSpec(
        "set_variant_selection",
        "Set Variant Selection",
        "Selects a variant of a variant set.",
        (
            STAGE_PARAM,
            PRIM_PARAM,
            SET_PARAM,
            Param("variant", STRING, "", "Variant to select, empty clears it."),
        ),
        STRING,
        ("composition", "variants"),
    ),
    OperationSpec(
        "get_variants",
        "Get Variants",
        "Describes the variant sets of a prim: their variants and selection.",
        (STAGE_PARAM, PRIM_PARAM),
        DICT,
        ("composition", "variants"),
    ),
    OperationSpec(
        "export_to_string",
        "Export To String",
        "Gets the USD text of a stage, optionally flattened into one layer.",
        (STAGE_PARAM, Param("flatten", BOOL, False, "Compose everything first.")),
        STRING,
        ("composition", "export"),
    ),
    OperationSpec(
        "flatten_stage",
        "Flatten Stage",
        "Composes a stage into one layer and writes it to a file.",
        (STAGE_PARAM, Param("path", STRING, "", "File to write.")),
        STRING,
        ("composition", "export"),
    ),
)
