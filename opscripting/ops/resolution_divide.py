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
    node.getParameter("location").setValue("/root", 0)

    userparam = node.getParameters().createChildGroup("user")
    p = userparam.createChildNumber("divider", 1)
    hint = {
        "help": (
            "<p>Amount to divide the current resolution by.<br>"
            "You can also specify it using a GSV named "
            "<code>resolution_divider</code>.</p>"
        )
    }
    p.setHintString(repr(hint))

    return node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()
