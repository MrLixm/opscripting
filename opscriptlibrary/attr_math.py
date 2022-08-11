import os.path

from Katana import NodegraphAPI

from customtooling.nodebase import createDefaultCustomTool

NAME = os.path.splitext(os.path.basename(__file__))[0]
VERSION = (1, 5, 1)


def createUserParam(userparam, set_as_expression=False):
    # type: (NodegraphAPI.Parameter, bool) -> None

    p = userparam.createChildStringArray("attributes", 2)
    p.setExpression("=^/user.attributes", set_as_expression)
    p.setTupleSize(2)
    hint = {
        "resize": True,
        "tupleSize": 2,
        "help": (
            "<p>n Rows of 2 columns:<br/>- [1*n] = path of the attribute relative"
            " to the location<br/>- [2*n] = expression to specify indesx to skip like"
            " :<br/>&nbsp;&nbsp; Every X indexes, skip indexes N[...] == N,N,.../X =="
            ' (%d+,*)+/%d+<br/>&nbsp;&nbsp; ex: skip 2/4st index every 4 index == "2,4/4"</p>    '
        ),
    }
    p.setHintString(repr(hint))

    p = userparam.createChildNumber("multiply", 1.0)
    p.setExpression("=^/user.multiply", set_as_expression)
    hint = {
        "slider": True,
        "slidermax": 10,
    }
    p.setHintString(repr(hint))

    p = userparam.createChildNumber("add", 0.0)
    p.setExpression("=^/user.add", set_as_expression)
    hint = {
        "slider": True,
        "slidermax": 10,
        "slidermin": -10,
    }
    p.setHintString(repr(hint))

    p = userparam.createChildString("op_order", "add")
    p.setExpression("=^/user.op_order", set_as_expression)
    hint = {
        "widget": "popup",
        "options": ["add", "multiply"],
        "help": "Which operation should be applied first.",
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
        description="Perform some basic math operation on attributes values.",
        version=VERSION,
    )

    configOpScript(nodetool.getDefaultOpScriptNode())
    configTool(node=nodetool.node)

    nodetool.getAboutParam().moveToBottom()
    return nodetool.node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()
