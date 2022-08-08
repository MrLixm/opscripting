import os.path

from Katana import NodegraphAPI

from opscripting.tooling import createDefaultCustomTool

NAME = os.path.splitext(os.path.basename(__file__))[0]
VERSION = "1.0.0"


def configOpScript(node):
    # type: (NodegraphAPI.Node) -> None
    script = """
local script = require("opscripting.tools.{NAME}")
script()"""
    script = script.format(NAME=NAME)

    node.getParameter("CEL").setExpression("=^/user.CEL", True)
    node.getParameter("applyWhere").setValue("at locations matching CEL", 0)
    node.getParameter("script.lua").setValue(script, 0)

    userparam = node.getParameter("user")
    p = userparam.createChildNumber("point_scale", 1)
    hint = {
        "slider": True,
        "help": "multiplier of the point's scale in the viewer",
        "sliderMax": 50,
    }
    p.setHintString(repr(hint))
    p.setExpression("=^/user.point_scale", True)
    return


def configTool(node):
    # type: (NodegraphAPI.Node) -> None

    userparam = node.getParameter("user")

    p = userparam.createChildString("CEL", "")
    hint = {"widget": "cel"}
    p.setHintString(repr(hint))

    p = userparam.createChildNumber("point_scale", 1)
    hint = {
        "slider": True,
        "help": "multiplier of the point's scale in the viewer",
        "sliderMax": 50,
    }
    p.setHintString(repr(hint))

    return


def build():
    # type: () -> NodegraphAPI.Node

    nodetool = createDefaultCustomTool(NAME)
    nodetool.setInfo(
        author="Liam Collod",
        description="Change scale of the geometry points.",
        version=VERSION,
    )

    configOpScript(nodetool.getDefaultOpScriptNode())
    configTool(node=nodetool.node)

    return nodetool.node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()
