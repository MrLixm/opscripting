class COLORS:
    """
    Colors for the entries in the LayeredMenu.
    """

    default = (0.39, 0.35, 0.466)  # Low contrast purple.


SHORTCUT = "S"
"""
Shortcut to use in the Nodegraph to make the LayeredMenu appears.
"""

ENVVAR_EXCLUDED_TOOLS = "OPSCRIPTTOOLS_EXCLUDED_TOOLS"
"""
Environment variable name that must specify a list of tools name to NOT show in
the LayeredMenu. Separator is the system path sperator (; or :):

ex: ``"attr_math;xform2P;point_width"``
"""
