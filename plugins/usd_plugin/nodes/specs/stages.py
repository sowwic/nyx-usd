from ..usd_node import OperationSpec, Param
from .common import STAGE_PARAM, STRING


SPECS: tuple[OperationSpec, ...] = (
    OperationSpec(
        "open_stage",
        "Open Stage",
        "Opens a USD file in the client.",
        (Param("path", STRING, "", "File to open."),),
        STRING,
        ("stage",),
    ),
    OperationSpec(
        "create_stage",
        "Create Stage",
        "Creates a stage in the client, in memory if no file is given.",
        (Param("path", STRING, "", "File to save the stage to, optional."),),
        STRING,
        ("stage",),
    ),
    OperationSpec(
        "save_stage",
        "Save Stage",
        "Saves a stage to its file, or exports it to the given one.",
        (
            STAGE_PARAM,
            Param("path", STRING, "", "File to export to, the stage file if empty."),
        ),
        STRING,
        ("stage",),
    ),
    OperationSpec(
        "close_stage",
        "Close Stage",
        "Closes a stage in the client without saving it.",
        (STAGE_PARAM,),
        tags=("stage",),
    ),
)
