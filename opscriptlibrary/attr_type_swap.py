import os.path

from Katana import NodegraphAPI

from opscripttools.tooling import createDefaultCustomTool

NAME = os.path.splitext(os.path.basename(__file__))[0]
VERSION = "1.0.2"


def createUserParam(userparam, set_as_expression=False):
    # type: (NodegraphAPI.Parameter, bool) -> None

    p = userparam.createChildStringArray("attributes", 2)
    p.setExpression("=^/user.attributes", set_as_expression)
    p.setTupleSize(2)
    hint = {
        "resize": True,
        "tupleSize": 2,
        "help": (
            "<p>n Rows of 2 columns:<br/>"
            "-[1 * n] = path of the attribute relative to the location<br/>"
            "-[2 * n] = new DataAttribute type to use, ex: StringAttribute<br/>"
            "<br/>"
            "DataAttributes available are:<br/>"
            "- IntAttribute<br/>-FloatAttribute<br/>-DoubleAttribute<br/>-StringAttribute"
        ),
    }
    p.setHintString(repr(hint))

    p = userparam.createChildString("method", "array")
    p.setExpression("=^/user.method", set_as_expression)
    hint = {
        "widget": "popup",
        "options": ["table", "array"],
        "help": (
            "<p>which method to use for querying attributes:<br/>"
            "- <code>table</code>: max of 2^27 (134 million) values per attribute<br/>"
            "- <code>array</code> <em>(default)</em>: a bit slower, no size limit</p>"
        ),
    }
    p.setHintString(repr(hint))

    return


def configOpScript(node):
    # type: (NodegraphAPI.Node) -> None

    script = """
local script = require("opscriptlibrary.{NAME}")
script()"""
    script = script.format(NAME=NAME)

    node.getParameter("CEL").setExpression("=^/user.CEL", True)
    node.getParameter("applyWhere").setValue("at locations matching CEL", 0)
    node.getParameter("script.lua").setValue(script, 0)
    userparam = node.getParameter("user")
    createUserParam(userparam, set_as_expression=True)
    return


def configTool(node):
    # type: (NodegraphAPI.Node) -> None

    userparam = node.getParameter("user")

    p = userparam.createChildString("CEL", "")
    hint = {"widget": "cel"}
    p.setHintString(repr(hint))

    createUserParam(userparam)
    return


def build():
    # type: () -> NodegraphAPI.Node

    nodetool = createDefaultCustomTool(NAME)
    nodetool.getAboutParam().update(
        author="Liam Collod",
        description="Change the type of an attribute. ex: FloatAttribute -> DoubleAttribute",
        version=VERSION,
    )

    configOpScript(nodetool.getDefaultOpScriptNode())
    configTool(node=nodetool.node)

    nodetool.getAboutParam().moveToBottom()
    return nodetool.node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()
