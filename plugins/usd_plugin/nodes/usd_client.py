from nyx.api.v1.std_nodes import LaunchProcessNode


CLIENT_SOURCE = """\
from nyx_bridge.client import NyxClient


class UsdClient(NyxClient):
    CLIENT_KIND = "usd"


UsdClient(name={name!r}, reconnect=False).serve_forever()
"""
"""Code of the client, `{name}` is the name it connects as.

The generic client of `nyx_bridge` with the kind `usd`. The address and the token come
from the environment the node sets.
"""

PYTHON_VARIABLE = "NYX_USD_PYTHON"
"""Environment variable naming the interpreter, used when the input is empty."""


class UsdClientNode(LaunchProcessNode):
    """Launch Process node starting a client in an interpreter that has USD.

    Builds the command itself: it runs the generic client of `nyx_bridge` in the
    interpreter. That interpreter needs `pxr`, `nyx_bridge` and `nyx_usd`, make them
    importable through its own packages or `PYTHONPATH` in `env`. The USD nodes go in a
    Remote Client node inside of this one.
    """

    DEFAULT_NAME = "usd_client"

    @classmethod
    def get_type_id(cls) -> str:
        """str: node type id."""
        return "usd:client"

    @classmethod
    def get_type_display_name(cls) -> str:
        """str: name shown in the UI."""
        return "USD Client"

    @classmethod
    def get_description(cls) -> str:
        """str: what the node type does, shown in the palette."""
        return (
            "Starts a Python interpreter that has USD as a client of the bridge, "
            "waits for it and stops it when the nodes inside are done."
        )

    @classmethod
    def get_type_icon(cls) -> str:
        """str: resource path of the type icon."""
        return ":/usd/icons/usd_32"

    @classmethod
    def get_tags(cls) -> set[str]:
        """set[str]: node tags."""
        return {"usd", "bridge", "scope"}

    def setup(self) -> None:
        """Add the components of Launch Process, the command being the interpreter."""
        super().setup()
        self.python_cpnt = self.command_cpnt
        self.python_cpnt.name = "python"
        self.python_cpnt.description = (
            f"Python interpreter that has USD. Empty uses ${PYTHON_VARIABLE} from the "
            "environment, or from `env`."
        )

    def _build_arguments(self, environment: dict) -> list[str]:
        """Get the command running the client in the interpreter.

        Args:
            environment (dict): variables of the process, the bridge ones included.

        Raises:
            ValueError: there is no interpreter set.

        Returns:
            list[str]: the arguments, the first one is the interpreter.
        """
        python = self.python_cpnt.pull_value() or environment.get(PYTHON_VARIABLE)
        if not python:
            raise ValueError(
                f"{self.name}: no interpreter, set `python` or ${PYTHON_VARIABLE}"
            )
        name = environment[self.CLIENT_NAME_VARIABLE]
        return [python, "-c", CLIENT_SOURCE.format(name=name)]
