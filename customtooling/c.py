"""
Constants
"""


class COLORS:
    """
    Colors for the entries in the LayeredMenu.
    Can also be used to color the node.

    Assumed to be sRGB - Display encoded.
    """

    white = (0.75, 0.75, 0.75)
    grey = (0.5, 0.5, 0.5)
    black = (0.015, 0.015, 0.015)

    green = (0.22, 0.46, 0.27)
    bluelight = (0.27, 0.43, 0.46)
    blue = (0.23, 0.27, 0.46)
    purple = (0.39, 0.35, 0.466)
    pink = (0.46, 0.27, 0.35)
    red = (0.46, 0.16, 0.18)
    yellow = (0.46, 0.41, 0.28)

    default = purple  # fallback if color not specified on subclass


ENVVAR_EXCLUDED_TOOLS = "CUSTOMTOOLING_EXCLUDED_TOOLS"
"""
Environment variable name that must specify a list of tools name to NOT show in
the LayeredMenu. Separator is the system path sperator (; or :):

ex: ``"attr_math;xform2P;point_width"``
"""

FLAVOR_NAME = "customTool"
"""
As each CustomTool is registered as a separate node type, to quickly find all the custom
tool, they are assigned a flavor using ``NodegraphAPI.AddNodeFlavor()``
"""


LAYEREDMENU_SHORTCUT = "O"
"""
Shortcut to use in the Nodegraph to make the LayeredMenu appears.
This is the LayeredMenu for ALL the tools that might be disabled.
"""
