import os.path

from Katana import NodegraphAPI


def build():
    # type: () -> NodegraphAPI.Node

    ops_name = os.path.splitext(os.path.basename(__file__))[0]

    script = """
local script = require("opscripting.ops.{NAME}")
script()"""
    script = script.format(NAME=ops_name)

    node = NodegraphAPI.CreateNode("OpScript", NodegraphAPI.GetRootNode())
    node.setName("OpScript_{}_1".format(ops_name))

    node.getParameter("applyWhere").setValue("at specific location", 0)
    node.getParameter("script.lua").setValue(script, 0)
    userparam = node.getParameters().createChildGroup("user")
    p = userparam.createChildStringArray("attributes", 2)
    p.setTupleSize(2)
    hint = {
        "resize": True,
        "tupleSize": 2,
        "help": (
            "<p>n Rows of 2 columns:<br />- [1*n] = path of the attribute relative"
            " to the location<br />- [2*n] = expression to specify indesx to skip like"
            " :<br />&nbsp;&nbsp; Every X indexes, skip indexes N[...] == N,N,.../X =="
            ' (%d+,*)+/%d+<br />&nbsp;&nbsp; ex: skip 2/4st index every 4 index == "2,4/4"</p>    '
        ),
    }
    p.setHintString(repr(hint))
    userparam.createChildNumber("multiply", 1.0)
    userparam.createChildNumber("add", 0.0)
    p = userparam.createChildString("op_order", "add")
    hint = {
        "widget": "popup",
        "options": ["add", "multiply"],
        "help": "Which operation should be applied first.",
    }
    p.setHintString(repr(hint))

    return node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()
