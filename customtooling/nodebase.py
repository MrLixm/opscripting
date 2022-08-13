import logging
import re
import traceback
from abc import abstractmethod
import inspect
from typing import Optional
from typing import Union
from typing import Tuple
from typing import List

from Katana import NodegraphAPI

from . import c
from . import util

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


def customToolNodeCallback(**kwargs):
    """
    This code is executed for ANY node created in the Nodegraph.
    We use it to modify the CustomToolNode apperance after its creation.

    THis is for operations that cannot be performed while the node instancing is not
    terminated like ``node.getAttributes()``.

    kwargs example ::

        {'node': <Xform2P Xform2P 'Xform2P_0002'>,
         'nodeName': 'Xform2P',
         'nodeType': 'Xform2P',
         'objectHash': -38886720}

    Args:
        **kwargs: see kwars example above
    """
    node = kwargs.get("node")
    if not isinstance(node, CustomToolNode):
        return

    attr = node.getAttributes()
    attr["ns_basicDisplay"] = 1  # remove group shape
    attr["ns_iconName"] = ""  # remove group icon
    node.setAttributes(attr)
    return


class CustomToolNode(NodegraphAPI.PythonGroupNode):
    """
    Abstract base class to create "CustomTool" nodes.

    That's just a group node with some standards like an "about" param.

    Its default structure correpond to one input and output port, and two dot nodes
    connected together in the inside.
    """

    Colors = c.COLORS  # convenience, to not have to import multiple module for use
    """
    All pre-defined color available to assign to this tool.
    """

    port_in_name = "in"
    port_out_name = "out"

    name = NotImplemented  # type: str
    version = NotImplemented  # type: Tuple[int,int,int]
    color = None  # type: Tuple[float,float,float]
    description = ""  # type: str
    author = ""  # type: str
    maintainers = []  # type: List[str]

    class AboutParamNames:
        root = "About"
        name = "name_"
        version = "version_"
        description = "info_"
        author = "author_"
        path = "path_"
        documentation = "open_documentation"

    def __init__(self):
        super(CustomToolNode, self).__init__()

        self._about_param = None  # type: NodegraphAPI.Parameter
        self._node_dot_up = None  # type: NodegraphAPI.Node
        self._node_dot_down = None  # type: NodegraphAPI.Node

        self._buildAboutParam()
        self._buildDefaultStructure()
        self._build()

    def _buildAboutParam(self):

        usergrp = self.getParameter("user")
        if not usergrp:
            usergrp = self.getParameters().createChildGroup("user")
            hint = {"hideTitle": True}
            usergrp.setHintString(repr(hint))

        param = usergrp.createChildGroup(self.AboutParamNames.root)

        p = param.createChildString(self.AboutParamNames.name, self.name)
        p.setHintString(repr({"readOnly": True}))

        p = param.createChildString(
            self.AboutParamNames.version, versionize(self.version)
        )
        p.setHintString(repr({"readOnly": True}))

        p = param.createChildString(self.AboutParamNames.description, self.description)
        p.setHintString(repr({"readOnly": True}))

        p = param.createChildString(self.AboutParamNames.author, self.author)
        p.setHintString(repr({"readOnly": True}))

        p = param.createChildString(
            self.AboutParamNames.path, inspect.getfile(self.__class__)
        )
        p.setHintString(repr({"readOnly": True, "widget": "null"}))

        p = param.createChildString(
            self.AboutParamNames.documentation, inspect.getfile(self.__class__)
        )
        hints = {
            "widget": "scriptButton",
            "scriptText": c.OPEN_DOCUMENTATION_SCRIPT.format(
                PATH_PARAM=self.AboutParamNames.path
            ),
        }
        p.setHintString(repr(hints))

        self._about_param = param
        return

    def _buildDefaultStructure(self):
        """
        Create the basic nodegraph representation of a custom tool.
        This is a styled GroupNode with an OpScript node connected inside.
        """

        self.addInputPort(self.port_in_name)
        self.addOutputPort(self.port_out_name)
        self.setName("{}_0001".format(self.name))

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

        self._node_dot_up = node_dot_up
        self._node_dot_down = node_dot_down
        return

    @classmethod
    def _check(cls):
        """
        Raise an error if the class is malformed.
        """

        util.asserting(
            isinstance(cls.name, str),
            "name=<{}> is not a str".format(cls.name),
        )
        util.asserting(
            False if re.search(r"\W", cls.name) else True,
            "name=<{}> contains unsupported characters".format(cls.name),
        )

        util.asserting(
            isinstance(cls.version, tuple) and len(cls.version) == 3,
            "version=<{}> is not a tuple or of length 3".format(cls.version),
        )
        util.asserting(
            not cls.color or isinstance(cls.color, tuple) and len(cls.color) == 3,
            "color=<{}> is not a tuple or of length 3".format(cls.color),
        )
        util.asserting(
            isinstance(cls.description, str),
            "description=<{}> is not a str".format(cls.description),
        )
        util.asserting(
            isinstance(cls.author, str),
            "author=<{}> is not a str".format(cls.author),
        )
        util.asserting(
            isinstance(cls.maintainers, (list, tuple)),
            "maintainers=<{}> is not a list or tuple".format(cls.maintainers),
        )

        return

    @abstractmethod
    def _build(self):
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

    def wireInsertNodes(self, node_list, vertical_offset=150):
        # type: (List[NodegraphAPI.Node], int) -> None
        """
        Utility method to quickly connect an ORDERED list of node to the internal network.
        The nodes are inserted after the port connected to Output Dot node.

        For convenience, it is assumed that nodes only have one input/output port.

        Args:
            vertical_offset:
                negative offset to apply to each node position in the nodegraph
            node_list:
                node to connect to the internal network and between each other, in
                the expected order.
        """
        # we have to make a big try/except block because Katana is shitty at catching
        # error of creation of registered Nodes.
        try:
            indownport = self._node_dot_down.getInputPortByIndex(0)
            previousOutPort = indownport.getConnectedPort(0)
            previousPos = NodegraphAPI.GetNodePosition(previousOutPort.getNode())
            indownport.disconnect(previousOutPort)

            for node in node_list:

                node.getInputPortByIndex(0).connect(previousOutPort)
                NodegraphAPI.SetNodePosition(
                    node,
                    (previousPos[0], previousPos[1] - vertical_offset),
                )

                previousOutPort = node.getOutputPortByIndex(0)
                previousPos = NodegraphAPI.GetNodePosition(node)
                continue

            indownport.connect(previousOutPort)
        except:
            traceback.print_exc()
            logger.exception(
                "[{}][wireInsertNodes] Error while trying to connect {}"
                "".format(self.__class__.__name__, node_list)
            )
            raise
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

    def _buildDefaultStructure(self):

        super(OpScriptTool, self)._buildDefaultStructure()

        self._node_opscript = NodegraphAPI.CreateNode("OpScript", self)
        self._node_opscript.setName("OpScript_{}_0001".format(self.name))
        self._node_opscript.getParameters().createChildGroup("user")

        self.wireInsertNodes([self._node_opscript])
        return

    @abstractmethod
    def _build(self):
        pass

    def getDefaultOpScriptNode(self):
        # type: () -> Optional[NodegraphAPI.Node]
        """
        Return the OpScript node created at init. BUt the node might have other
        OpScript node inside.
        """
        return self._node_opscript
