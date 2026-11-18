import copy
import dataclasses
import typing

from nyx.api.v1 import CoreDatatypes, CoreNodeComponents
from nyx.api.v1.std_nodes import RemoteActionNode


@dataclasses.dataclass(frozen=True)
class Param:
    """Input of a USD node, an argument of the operation.

    Attributes:
        name: argument name of the operation, also the component name
        datatype: datatype id of the component
        default: initial value
        description: what the argument is
    """

    name: str
    datatype: str
    default: typing.Any = ""
    description: str = ""


@dataclasses.dataclass(frozen=True)
class OperationSpec:
    """Describes the node of an operation of `nyx_usd.ops`.

    Attributes:
        name: name of the function in `nyx_usd.ops`
        display_name: name shown in the UI
        description: what the node does
        params: inputs, in the order of the arguments
        result: datatype id of the response
        tags: what the operation is about, like `prim` or `composition`: the palette
            can be searched by them (`tags:prim`)
    """

    name: str
    display_name: str
    description: str
    params: tuple[Param, ...] = ()
    result: str = CoreDatatypes.OBJECT.value
    tags: tuple[str, ...] = ()


class UsdNode(RemoteActionNode):
    """Remote Action node calling one operation of `nyx_usd.ops`.

    Subclasses are made by `create_node_class`. The operation gets the inputs as
    keyword arguments and its return value ends up in `response`. The node has to be
    inside a Remote Client node whose client can import `nyx_usd`.
    """

    SPEC: OperationSpec

    @classmethod
    def get_type_id(cls) -> str:
        """str: node type id."""
        return f"usd:{cls.SPEC.name}"

    @classmethod
    def get_type_display_name(cls) -> str:
        """str: name shown in the UI."""
        return cls.SPEC.display_name

    @classmethod
    def get_description(cls) -> str:
        """str: what the node type does, shown in the palette."""
        return cls.SPEC.description

    @classmethod
    def get_type_icon(cls) -> str:
        """str: resource path of the type icon."""
        return ":/usd/icons/usd_32"

    @classmethod
    def get_tags(cls) -> set[str]:
        """set[str]: node tags."""
        return {"usd", "bridge", *cls.SPEC.tags}

    def setup(self) -> None:
        """Add the flow, one input per argument, the timeout and the response."""
        self.flow_cpnt = self.components_model.create_component(CoreNodeComponents.FLOW)
        self.flow_cpnt.name = "flow"
        self.flow_cpnt.readable = True
        self.flow_cpnt.writable = True
        self.components_model.add_component(self.flow_cpnt)

        self.param_cpnts = {}
        for param in self.SPEC.params:
            component = self._create_input(
                param.name,
                param.description,
                param.datatype,
                copy.deepcopy(param.default),
                literal=param.datatype == CoreDatatypes.STRING,
            )
            self.param_cpnts[param.name] = component
            self.components_model.add_component(component)

        self.timeout_cpnt = self._create_input(
            "timeout",
            "Seconds to wait for the answer before failing. 0 or less waits forever.",
            CoreDatatypes.FLOAT,
            self.DEFAULT_TIMEOUT,
        )
        self.components_model.add_component(self.timeout_cpnt)

        self.response_cpnt = self.components_model.create_component(
            CoreNodeComponents.VALUE
        )
        self.response_cpnt.name = "response"
        self.response_cpnt.description = "What the operation returned."
        self.response_cpnt.readable = True
        self.response_cpnt.is_editable = False
        self.response_cpnt.set_datatype(self.SPEC.result)
        self.components_model.add_component(self.response_cpnt)

    def _create_input(
        self, name: str, description: str, datatype: str, default, literal: bool = False
    ):
        """Create an editable input value component.

        Args:
            name (str): component name.
            description (str): component description.
            datatype (str): datatype id.
            default (Any): initial value.
            literal (bool): keep text as typed instead of evaluating it.

        Returns:
            NodeComponent: new component, not added to the node yet.
        """
        component = self.components_model.create_component(CoreNodeComponents.VALUE)
        component.name = name
        component.description = description
        component.is_editable = True
        component.writable = True
        component.is_literal = literal
        component.set_datatype(datatype)
        component.push_value(default)
        return component

    def build_args(self) -> dict[str, typing.Any]:
        """Get the arguments of the operation.

        Returns:
            dict[str, Any]: input values by argument name.
        """
        return {name: cpnt.pull_value() for name, cpnt in self.param_cpnts.items()}

    def build_script(self, args: dict[str, typing.Any]) -> str:
        """Get the code calling the operation in the client.

        Args:
            args (dict[str, Any]): the variables the code will see.

        Returns:
            str: source code.
        """
        names = list(args)
        return (
            "import nyx_usd.ops\n"
            f"result = nyx_usd.ops.{self.SPEC.name}"
            f"(**{{name: globals()[name] for name in {names!r}}})\n"
        )


def create_node_class(spec: OperationSpec) -> type[UsdNode]:
    """Create the node class of an operation.

    Args:
        spec (OperationSpec): operation to wrap.

    Returns:
        type[UsdNode]: node class.
    """
    class_name = "Usd" + spec.display_name.replace(" ", "") + "Node"
    return type(
        class_name,
        (UsdNode,),
        {"SPEC": spec, "DEFAULT_NAME": spec.name, "__doc__": spec.description},
    )
