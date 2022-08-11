import logging
from abc import abstractmethod
from typing import Optional
from typing import Union
from typing import Tuple
from typing import List

from Katana import NodegraphAPI

__all__ = (
    "CustomToolNode",
    "OpScriptTool",
)

logger = logging.getLogger(__name__)


VersionableType = Union[str, Union[List[int], Tuple[int, int, int]]]


def versionize(version):
    # type: (VersionableType) -> str
    """
    Convert an object representing a potential version to a string representing
    the version.

    ex: (1,5,2) -> "1.5.2"
    """

    if isinstance(version, str):
        return version

    if isinstance(version, (tuple, list)) and len(version) == 3:
        version = map(str, version)
        return ".".join(version)

    raise TypeError(
        "Can't create a version object from arg <{}> of type {}"
        "".format(version, type(version))
    )


class CustomToolNode(NodegraphAPI.PythonGroupNode):
    """
    Abstract base class to create "CustomTool" nodes.

    That's just a group node with some standards like an "about" param.

    Its default structure correpond to one input and output port, and two dot nodes
    connected together in the inside.
    """

    port_in_name = "in"
    port_out_name = "out"

    name = NotImplemented  # type: str
    version = NotImplemented  # type: Tuple[int,int,int]
    color = None  # type: Tuple[float,float,float]
    description = ""  # type: str
    author = ""  # type: str
    maintainers = []  # type: List[str]

    def __init__(self):
        super(CustomToolNode, self).__init__()

        self._about_param = None  # type: NodegraphAPI.Parameter
        self.__buildAboutParam()
        self.__buildDefaultStructure()
        self.__build()

    def __buildDefaultStructure(self):
        """
        Create the basic nodegraph representation of a custom tool.
        This is a styled GroupNode with an OpScript node connected inside.
        """

        self.addInputPort(self.port_in_name)
        self.addOutputPort(self.port_out_name)
        self.setName("{}_0001".format(self.name))

        # attr = self.getAttributes()
        # attr["ns_basicDisplay"] = 1  # remove group shape
        # attr["ns_iconName"] = ""  # remove group icon
        # self.setAttributes(attr)

        pos = NodegraphAPI.GetNodePosition(self)

        node_dot_up = NodegraphAPI.CreateNode("Dot", self)
        NodegraphAPI.SetNodePosition(node_dot_up, (pos[0], pos[1] + 150))
        node_dot_up.setName("In_{}_0001".format(self.name))

        node_dot_down = NodegraphAPI.CreateNode("Dot", self)
        NodegraphAPI.SetNodePosition(node_dot_down, (pos[0], pos[1] - 150))
        node_dot_down.setName("Out_{}_0001".format(self.name))

        port_a = self.getSendPort(self.port_in_name)
        port_b = node_dot_up.getInputPortByIndex(0)
        port_a.connect(port_b)

        port_a = node_dot_up.getOutputPortByIndex(0)
        port_b = node_dot_down.getInputPortByIndex(0)
        port_a.connect(port_b)

        port_a = node_dot_down.getOutputPortByIndex(0)
        port_b = self.getReturnPort(self.port_out_name)
        port_a.connect(port_b)

        return

    def __buildAboutParam(self):

        usergrp = self.getParameter("user")
        if not usergrp:
            usergrp = self.getParameters().createChildGroup("user")
            hint = {"hideTitle": True}
            usergrp.setHintString(repr(hint))

        self._about_param = usergrp.createChildGroup(self.Names.root)
        self._about_param.createChildString(self.Names.name, self.name)
        self._about_param.createChildString(
            self.Names.version, versionize(self.version)
        )
        self._about_param.createChildString(self.Names.description, self.description)
        self._about_param.createChildString(self.Names.author, self.author)
        return

    @abstractmethod
    def __build(self):
        pass

    @property
    def user_param(self):
        # type: () -> NodegraphAPI.Parameter
        return self.getParameter("user")

    def moveAboutParamToBottom(self):
        """
        Move the AboutParam parameter to the bottom of the `user` parameter layout.
        """
        self.user_param.reorderChild(
            self._about_param,
            self.user_param.getNumChildren() - 1,
        )
        return


class OpScriptTool(CustomToolNode):
    """
    Abstract class to create a tool based on at least one OpScript node.
    The OpScript configuration (OpArg) is accessible to the user via parameters
    declared in the ``__build()`` method that must be overriden.
    """

    luamodule = NotImplemented
    """
    Every OpScript must live in a .lua registered in the LUA_PATH.
    This means the OpScript.script will only import it using ``require()``
    """

    def __buildDefaultStructure(self):

        super(OpScriptTool, self).__buildDefaultStructure()

        self._node_opscript = NodegraphAPI.CreateNode("OpScript", self)
        self._node_opscript.setName("OpScript_{}_0001".format(self.name))
        self._node_opscript.getParameters().createChildGroup("user")

        NodegraphAPI.PackageSuperToolAPI.NodeUtils.WireInlineNodes(
            parentGroupNode=self,
            nodes=self.getChildren(),
            x=150,
        )
        return

    @abstractmethod
    def __build(self):
        pass

    def getDefaultOpScriptNode(self):
        # type: () -> Optional[NodegraphAPI.Node]
        """
        Return the OpScript node created at init. BUt the node might have other
        OpScript node inside.
        """
        return self._node_opscript
