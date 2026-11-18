"""The operations of `nyx_usd.ops` that have a node, and their inputs.

One module per area in `specs/`. The arguments of a spec have to match the ones of the
function, in the same order.
"""

from .specs import attributes, composition, geometry, prims, stage_settings, stages
from .usd_node import OperationSpec


OPERATIONS: tuple[OperationSpec, ...] = (
    *stages.SPECS,
    *prims.SPECS,
    *attributes.SPECS,
    *stage_settings.SPECS,
    *composition.SPECS,
    *geometry.SPECS,
)
