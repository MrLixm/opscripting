import logging
from abc import abstractmethod
from typing import Optional
from typing import Union
from typing import Tuple
from typing import List

from Katana import NodegraphAPI

__all__ = (
    "AboutParam",
    "CustomTool",
    "addAboutParamToNode",
)

logger = logging.getLogger(__name__)


VersionableType = Union[str, Union[List[int], Tuple[int, int, int]]]


def versionize(version):
    # type: (VersionableType) -> str

    if isinstance(version, str):
        return version

    if isinstance(version, (tuple, list)) and len(version) == 3:
        version = map(str, version)
        return ".".join(version)

    raise TypeError(
        "Can't create a version object from arg <{}> of type {}"
        "".format(version, type(version))
    )


class AboutParam:
    class Names:

        root = "about"
        name = "name_"
        version = "version_"
        description = "info_"
        author = "author_"

    def __init__(self, node):
        # type: (NodegraphAPI.Node) -> None

        self.param = node.getParameter("user.{}".format(self.Names.root))

        assert self.param, "user.{} doesn't exists on node {}".format(
            self.Names.root, node
        )

        self.name = self.param.getChild(self.Names.name)
        self.version = self.param.getChild(self.Names.version)
        self.description = self.param.getChild(self.Names.description)
        self.author = self.param.getChild(self.Names.author)

        return

    def moveToBottom(self):
        """
        Move the AboutParam parameter to the bottom of the `user` parameter layout.
        """
        parent = self.param.getParent()
        parent.reorderChild(self.param, parent.getNumChildren() - 1)
        return

    def update(self, name="", version="", description="", author=""):
        # type: (str, VersionableType, str, str) -> None
        if name:
            self.name.setValue(name, 0)
        if version:
            self.version.setValue(versionize(version), 0)
        if description:
            self.description.setValue(description, 0)
        if author:
            self.author.setValue(author, 0)
        return

    @classmethod
    def createOn(cls, node, name="", version="0.1.0", description="", author=""):
        # type: (NodegraphAPI.Node, str, VersionableType, str, str) -> AboutParam

        usergrp = node.getParameter("user")
        if not usergrp:
            usergrp = node.getParameters().createChildGroup("user")
            hint = {"hideTitle": True}
            usergrp.setHintString(repr(hint))

        assert not node.getParameter(
            "user.{}".format(cls.Names.root)
        ), "user.{} already exists on node {}".format(cls.Names.root, node)

        aboutgrp = usergrp.createChildGroup(cls.Names.root)
        aboutgrp.createChildString(cls.Names.name, name)
        aboutgrp.createChildString(cls.Names.version, versionize(version))
        aboutgrp.createChildString(cls.Names.description, description)
        aboutgrp.createChildString(cls.Names.author, author)
        return AboutParam(node)


class CustomTool(NodegraphAPI.PythonGroupNode):

    port_in_name = "in"
    port_out_name = "out"

    name = NotImplemented
    color = None
    version = NotImplemented
    luamodule = None

    def __init__(self):
        super(CustomTool, self).__init__()

        self.buildDefaultStructure()
        self.__build()

    def buildDefaultStructure(self):
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

        addAboutParamToNode(self, self.name)

        node_opscript = NodegraphAPI.CreateNode("OpScript", self)
        node_opscript.setName("OpScript_{}_0001".format(self.name))
        node_opscript.getParameters().createChildGroup("user")

        pos = NodegraphAPI.GetNodePosition(self)

        node_dot_up = NodegraphAPI.CreateNode("Dot", self)
        NodegraphAPI.SetNodePosition(node_dot_up, (pos[0], pos[1] + 150))
        node_dot_up.setName("Dot_{}_0001".format(self.name))

        node_dot_down = NodegraphAPI.CreateNode("Dot", self)
        NodegraphAPI.SetNodePosition(node_dot_down, (pos[0], pos[1] - 150))
        node_dot_down.setName("Dot_{}_0001".format(self.name))

        port_a = self.getSendPort(self.port_in_name)
        port_b = node_dot_up.getInputPortByIndex(0)
        port_a.connect(port_b)

        port_a = node_dot_up.getOutputPortByIndex(0)
        port_b = node_opscript.getInputPortByIndex(0)
        port_a.connect(port_b)

        port_a = node_opscript.getOutputPortByIndex(0)
        port_b = node_dot_down.getInputPortByIndex(0)
        port_a.connect(port_b)

        port_a = node_dot_down.getOutputPortByIndex(0)
        port_b = self.getReturnPort(self.port_out_name)
        port_a.connect(port_b)

        return

    @abstractmethod
    def __build(self):
        pass

    def getUserParam(self):
        # type: () -> NodegraphAPI.Parameter
        return self.getParameter("user")

    def getAboutParam(self):
        # type: () -> AboutParam
        return AboutParam(node=self)

    def setVersion(self, version):
        # type: (VersionableType) -> None
        """
        Set the tool version on the ``user.about.version_`` parameter.

        Args:
            version: ex: "0.1.0"
        """
        self.getAboutParam().update(version=version)

    def getDefaultOpScriptNode(self):
        # type: () -> Optional[NodegraphAPI.Node]
        children = self.getChildren()
        for child in children:
            if child.getType() == "OpScript":
                return child
        return


def addAboutParamToNode(node, name="", version="0.1.0", description="", author=""):
    # type: (NodegraphAPI.Node, str, VersionableType, str, str) -> AboutParam
    """
    Add the "about" group parameter to the given node.
    This is added on custom tool to better track their origin.

    This section contains 4 params::

        ["name_", "version_", "info_", "author_"]

    Args:
        node: node to add the "user.about" parameter on.
        name: name of the tool
        version: version of the tool
        description: short describtion about what the tool does
        author: initial author of the tool
    """
    return AboutParam.createOn(node, name, version, description, author)
