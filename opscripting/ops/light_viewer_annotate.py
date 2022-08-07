import os.path

from Katana import NodegraphAPI


NAME = os.path.splitext(os.path.basename(__file__))[0]
VERSION = "1.5.0"


def createOpScript(parent):
    # type: (NodegraphAPI.GroupNode) -> NodegraphAPI.Node

    script = """
local script = require("opscripting.ops.{NAME}")
script()"""
    script = script.format(NAME=NAME)

    node = NodegraphAPI.CreateNode("OpScript", parent)
    node.setName("OpScript_lgva_0001")

    node.getParameter("CEL").setExpression("=^/user.CEL", True)
    node.getParameter("applyWhere").setValue("at locations matching CEL", 0)
    node.getParameter("script.lua").setValue(script, 0)

    userparam = node.getParameters().createChildGroup("user")
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

    return node


def createGroupNode():

    node = NodegraphAPI.CreateNode("Group", NodegraphAPI.GetRootNode())
    node.addInputPort("in")
    node.addOutputPort("out")
    node.setName("{}_0001".format(NAME.capitalize()))

    attr = node.getAttributes()
    attr["ns_basicDisplay"] = 1  # remove group shape
    attr["ns_iconName"] = ""  # remove group icon
    node.setAttributes(attr)

    userparam = node.getParameters().createChildGroup("user")
    hint = {"hideTitle": True}
    userparam.setHintString(repr(hint))

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

    pgrp = userparam.createChildGroup("about")
    pgrp.createChildString("author_", "Liam Collod")
    pgrp.createChildString(
        "info_", "Annotate (& color) lights in the viewer using their attributes."
    )
    pgrp.createChildString("version_", str(VERSION))

    return node


def build():
    # type: () -> NodegraphAPI.Node

    node = createGroupNode()

    # Create content of the Group

    node_opscript = createOpScript(node)
    pos = NodegraphAPI.GetNodePosition(node)

    node_dot_up = NodegraphAPI.CreateNode("Dot", node)
    NodegraphAPI.SetNodePosition(node_dot_up, (pos[0], pos[1] + 150))

    node_dot_down = NodegraphAPI.CreateNode("Dot", node)
    NodegraphAPI.SetNodePosition(node_dot_down, (pos[0], pos[1] - 150))

    port_a = node.getSendPort("in")
    port_b = node_dot_up.getInputPortByIndex(0)
    port_a.connect(port_b)

    port_a = node_dot_up.getOutputPortByIndex(0)
    port_b = node_opscript.getInputPortByIndex(0)
    port_a.connect(port_b)

    port_a = node_opscript.getOutputPortByIndex(0)
    port_b = node_dot_down.getInputPortByIndex(0)
    port_a.connect(port_b)

    port_a = node_dot_down.getOutputPortByIndex(0)
    port_b = node.getReturnPort("out")
    port_a.connect(port_b)

    return node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()
