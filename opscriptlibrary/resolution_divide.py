import os.path

from Katana import NodegraphAPI

NAME = os.path.splitext(os.path.basename(__file__))[0]
VERSION = "1.0.1"


def build():
    # type: () -> NodegraphAPI.Node

    script = """
local script = require("opscriptlibrary.{NAME}")
script()"""
    script = script.format(NAME=NAME)

    node = NodegraphAPI.CreateNode("OpScript", NodegraphAPI.GetRootNode())
    node.setName("OpScript_{}_1".format(NAME))

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
