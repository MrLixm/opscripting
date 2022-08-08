import os.path

from Katana import NodegraphAPI

from opscripttools.tooling import createDefaultCustomTool


NAME = os.path.splitext(os.path.basename(__file__))[0]
VERSION = "1.5.0"


def configOpScript(node):
    # type: (NodegraphAPI.Node) -> NodegraphAPI.Node
    """
    Args:
        node: an already existing OpScript node
    """

    script = """
local script = require("opscriptlibrary.{NAME}")
script()"""
    script = script.format(NAME=NAME)

    node.getParameter("CEL").setExpression("=^/user.CEL", True)
    node.getParameter("applyWhere").setValue("at locations matching CEL", 0)
    node.getParameter("script.lua").setValue(script, 0)

    userparam = node.getParameter("user")
    p = userparam.createChildString(
        "annotation_template", "<name> e:<exposure> <color>"
    )
    p.setExpression("=^/user.annotation", True)

    p = userparam.createChildNumber("annotation_colored", 0)
    p.setExpression("=^/user.color.annotations_colored", True)
    hint = {"widget": "boolean"}
    p.setHintString(repr(hint))

    p = userparam.createChildNumber("lights_colored", 0)
    p.setExpression("=^/user.color.lights_colored", True)
    hint = {"widget": "boolean"}
    p.setHintString(repr(hint))

    p = userparam.createChildNumber("color_hue", 1)
    p.setExpression("=^/user.color.hue", True)
    p = userparam.createChildNumber("color_saturation", 1)
    p.setExpression("=^/user.color.saturation", True)
    p = userparam.createChildNumber("color_value", 1)
    p.setExpression("=^/user.color.value", True)

    return


def configNodeTool(nodetool):

    userparam = nodetool.getUserParam()

    p = userparam.createChildString("annotation", "<name> e:<exposure> <color>")
    hint = {
        "help": (
            "<p>This string is build using tokens (ex: &lt;token&gt;)</p>"
            "<p>Tokens available depends on the script configuration but the default ones implemented are :</p>"
            "<p><em><code> name, color, exposure, intensity, aov, samples</code><br /></em></p>"
        )
    }
    p.setHintString(repr(hint))

    p = userparam.createChildString("CEL", '((/root/world/lgt//*{@type == "light"}))')
    hint = {
        "help": "<p>Make sure the locations matched by CEL are <b>only</b> lights.</p>",
        "widget": "cel",
    }
    p.setHintString(repr(hint))

    pgrp = userparam.createChildGroup("color")
    p = pgrp.createChildNumber("annotations_colored", 0)
    hint = {"widget": "boolean"}
    p.setHintString(repr(hint))

    p = pgrp.createChildNumber("lights_colored", 0)
    hint = {"widget": "boolean"}
    p.setHintString(repr(hint))

    p = pgrp.createChildNumber("hue", 1)
    hint = {
        "slider": True,
        "slidermax": 2.0,
        "help": "<p>&lt;H&gt;SV : hue. Only affect color in viewer.</p><p>1=no hue modification.</p>",
    }
    p.setHintString(repr(hint))

    p = pgrp.createChildNumber("saturation", 1)
    hint = {
        "slider": True,
        "slidermax": 2.0,
        "help": "<p>H&lt;S&gt;V : saturation. Only affect color in viewer.</p>",
    }
    p.setHintString(repr(hint))

    p = pgrp.createChildNumber("value", 1)
    hint = {
        "slider": True,
        "slidermax": 2.0,
        "help": "<p>HS&lt;V&gt; : value. Only affect color in viewer.</p>",
    }
    p.setHintString(repr(hint))

    return


def build():
    # type: () -> NodegraphAPI.Node

    nodetool = createDefaultCustomTool(name=NAME)
    nodetool.setInfo(
        author="Liam Collod",
        description="Annotate (& color) lights in the viewer using their attributes.",
        version=VERSION,
    )
    configNodeTool(nodetool)
    configOpScript(nodetool.getDefaultOpScriptNode())

    return nodetool.node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()
