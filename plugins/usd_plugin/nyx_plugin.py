"""Nyx plugin with nodes running `nyx_usd.ops` in a bridge client.

Loaded by Nyx, so it never imports `pxr`: the operations run in the client of the
enclosing Remote Client node, an interpreter that has USD. Add the `plugins` folder
of the repository to `NYX_PLUGIN_PATH`.
"""

import typing

from nyx.api.v1 import NyxPlugin, NyxPluginManager

from .resources import resources_rc  # noqa: F401
from .nodes.operations import OPERATIONS
from .nodes.usd_client import UsdClientNode
from .nodes.usd_node import create_node_class


@NyxPluginManager.register_plugin()
class NyxUsd(NyxPlugin):
    """Plugin providing nodes for USD operations run in a bridge client."""

    @classmethod
    def get_type_id(cls) -> str:
        """str: plugin id."""
        return "NyxUsd"

    @classmethod
    def get_type_display_name(cls) -> str:
        """str: name shown in the UI."""
        return "USD"

    @classmethod
    def initialize(cls) -> typing.Self:
        """Create the plugin with the nodes.

        Returns:
            typing.Self: initialized plugin.
        """
        plugin = cls()
        plugin.contents.nodes.append(UsdClientNode)
        plugin.contents.nodes.extend(create_node_class(spec) for spec in OPERATIONS)
        return plugin
