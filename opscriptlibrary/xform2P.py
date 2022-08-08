import os.path

from Katana import NodegraphAPI

from opscripttools.tooling import createDefaultCustomTool

NAME = os.path.splitext(os.path.basename(__file__))[0]
VERSION = "1.0.0"


def configOpScript(node):
    # type: (NodegraphAPI.Node) -> None

    script = """
local script = require("opscriptlibrary.{NAME}")
script()"""
    script = script.format(NAME=NAME)

    node.getParameter("CEL").setExpression("=^/user.CEL", True)
    node.getParameter("applyWhere").setValue("at locations matching CEL", 0)
    node.getParameter("script.lua").setValue(script, 0)
    return


def configTool(node):
    # type: (NodegraphAPI.Node) -> None

    userparam = node.getParameter("user")

    p = userparam.createChildString("CEL", "")
    hint = {"widget": "cel"}
    p.setHintString(repr(hint))

    return


def build():
    # type: () -> NodegraphAPI.Node

    nodetool = createDefaultCustomTool(NAME)
    nodetool.getAboutParam().update(
        author="Liam Collod",
        description="Merge xform transformations to the geometry.point.P attribute.",
        version=VERSION,
    )

    configOpScript(nodetool.getDefaultOpScriptNode())
    configTool(node=nodetool.node)

    nodetool.getAboutParam().moveToBottom()
    return nodetool.node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()
