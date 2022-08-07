import os.path

from Katana import NodegraphAPI

NAME = os.path.splitext(os.path.basename(__file__))[0]
VERSION = "1.0.1"


def build():
    # type: () -> NodegraphAPI.Node

    script = """
local script = require("opscripting.ops.{NAME}")
script()"""
    script = script.format(NAME=NAME)

    node = NodegraphAPI.CreateNode("OpScript", NodegraphAPI.GetRootNode())
    node.setName("OpScript_{}_1".format(NAME))

    node.getParameter("applyWhere").setValue("at specific location", 0)
    node.getParameter("script.lua").setValue(script, 0)

    userparam = node.getParameters().createChildGroup("user")
    p = userparam.createChildStringArray("attributes", 2)
    p.setTupleSize(2)
    hint = {
        "resize": True,
        "tupleSize": 2,
    }
    p.setHintString(repr(hint))
    p = userparam.createChildString("method", "array")
    hint = {
        "widget": "popup",
        "options": ["table", "array"],
        "help": """
        <p>which method to use for querying attributes:<br />- <code>table</code> : max of 2^27 (134 million) values per attribute<br />- <code>array</code> <em>(default)</em>: a bit slower, no size limit</p>
        """,
    }
    p.setHintString(repr(hint))

    return node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()
