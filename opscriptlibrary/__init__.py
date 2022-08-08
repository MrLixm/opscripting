"""
The goal is to have every "node creation" module available in this namespace.
So we can iterate over this package to retrieve all the nodes to create.

This mean you can create tools in subdirectory as long as they are imported here like::

    from opscripttools.tools.myCategory import *

This also means that you could tools even from an external package, as long as it
has been added to the LUA_PATH and PYTHONPATH.

**DO NOT import anything else than "node creation" module**

All module are expected to have a build() function. See doc for details.

..
    TODO maybe find a batter alternative than a wildcard import ?
    This is the most convenient way for now, and anyway the package is not really used
    directly, it is just "batch iterated".
"""
from . import *
