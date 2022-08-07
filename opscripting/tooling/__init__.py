import logging
from typing import Optional

from Katana import NodegraphAPI

__all__ = (
    "CustomTool",
    "addAboutToNode",
    "createDefaultCustomTool",
)

logger = logging.getLogger(__name__)


def addAboutToNode(node, name, version, description="", author=""):
    # type: (NodegraphAPI.Node, str, str, str, str) -> None
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

    usergrp = node.getParameter("user")
    if not usergrp:
        usergrp = node.getParameters().createChildGroup("user")
        hint = {"hideTitle": True}
        usergrp.setHintString(repr(hint))

    aboutgrp = usergrp.createChildGroup("about")
    aboutgrp.createChildString("name_", name)
    aboutgrp.createChildString("version_", version)
    aboutgrp.createChildString("info_", description)
    aboutgrp.createChildString("author_", author)
    return


def createDefaultCustomTool(name):
    # type: (str) -> CustomTool
    """
    Create and return a default custom tool node with a basic setup.
    """
    return CustomTool.createDefault(name)


class CustomTool(object):

    port_in_name = "in"
    port_out_name = "out"

    def __init__(self, node, name):
        self.name = name
        self.node = node

    @classmethod
    def createDefault(cls, name):
        # type: (str) -> CustomTool
        """
        Create the basic nodegraph representation of a custom tool.
        This is a styled GroupNode with an OpScript node connected inside.
        """

        node_root = NodegraphAPI.CreateNode("Group", NodegraphAPI.GetRootNode())
        node_root.addInputPort(cls.port_in_name)
        node_root.addOutputPort(cls.port_out_name)
        node_root.setName("{}_0001".format(name.capitalize()))

        attr = node_root.getAttributes()
        attr["ns_basicDisplay"] = 1  # remove group shape
        attr["ns_iconName"] = ""  # remove group icon
        node_root.setAttributes(attr)

        addAboutToNode(node_root, name, "0.1.0")

        node_opscript = NodegraphAPI.CreateNode("OpScript", node_root)
        node_opscript.setName("OpScript_{}_0001".format(name))
        node_opscript.getParameters().createChildGroup("user")

        pos = NodegraphAPI.GetNodePosition(node_root)

        node_dot_up = NodegraphAPI.CreateNode("Dot", node_root)
        NodegraphAPI.SetNodePosition(node_dot_up, (pos[0], pos[1] + 150))
        node_dot_up.setName("Dot_{}_0001".format(name))

        node_dot_down = NodegraphAPI.CreateNode("Dot", node_root)
        NodegraphAPI.SetNodePosition(node_dot_down, (pos[0], pos[1] - 150))
        node_dot_down.setName("Dot_{}_0001".format(name))

        port_a = node_root.getSendPort(cls.port_in_name)
        port_b = node_dot_up.getInputPortByIndex(0)
        port_a.connect(port_b)

        port_a = node_dot_up.getOutputPortByIndex(0)
        port_b = node_opscript.getInputPortByIndex(0)
        port_a.connect(port_b)

        port_a = node_opscript.getOutputPortByIndex(0)
        port_b = node_dot_down.getInputPortByIndex(0)
        port_a.connect(port_b)

        port_a = node_dot_down.getOutputPortByIndex(0)
        port_b = node_root.getReturnPort(cls.port_out_name)
        port_a.connect(port_b)

        return CustomTool(node=node_root, name=name)

    def getUserParam(self):
        # type: () -> NodegraphAPI.Parameter
        return self.node.getParameter("user")

    def setVersion(self, version):
        # type: (str) -> None
        """
        Set the tool version on the ``user.about.version_`` parameter.

        Args:
            version: ex: "0.1.0"
        """

        self.getUserParam().getChild("version_").setValue(version, 0)

    def getDefaultOpScriptNode(self):
        # type: () -> Optional[NodegraphAPI.Node]
        children = self.node.getChildren()
        for child in children:
            if child.getType() == "OpScript":
                return child
        return
