import logging
import pkgutil
import sys
import traceback
from types import ModuleType
from typing import Dict
from typing import Type
from typing import Optional

if sys.version_info[0] == 2:
    from pkgutil import ImpImporter as FileFinder
else:
    from importlib.machinery import FileFinder

from Katana import NodegraphAPI
from Katana import LayeredMenuAPI

from . import c
from . import tooling

__all__ = (
    "getAllTools",
    "getAvailableTools",
    "getLayeredMenu",
    "registerTools",
)

logger = logging.getLogger(__name__)


REGISTERED = False


def getAllTools():
    # type: () -> Dict[str, Type[tooling.CustomToolNode]]
    """
    Get a list of all the "tools" modules available.

    Not recommended to use directly. See ``getAvailableTools()`` instead.

    SRC: https://stackoverflow.com/a/1310912/13806195
    """

    def loadModule(module_loader_, module_name_):
        # type: (FileFinder, str) -> Optional[ModuleType]
        """
        Python 2 and 3 compatible.
        """
        try:
            module_ = module_loader_.find_module(module_name_).load_module(module_name_)
        except Exception as excp:
            logger.error(
                "[getAllTools][_loadModule] Cannot load <{}>: {}"
                "".format(module_name_, excp)
            )
            return

        return module_

    import os  # defer import to get the latest version of os.environ
    import opscriptlibrary

    out = dict()
    pkgpath = os.path.dirname(opscriptlibrary.__file__)

    for module_loader, name, ispkg in pkgutil.iter_modules([pkgpath]):

        # tools can only be modules
        if ispkg:
            continue

        module = loadModule(module_loader, name)
        if not module:
            continue

        try:
            node_class = module.NODE
        except AttributeError:
            logger.error(
                "[getAllTools] tool module <{}> doesn't declare the NODE variable."
                "".format(name)
            )
            continue

        if not issubclass(node_class, tooling.CustomToolNode):
            logger.error(
                "[getAllTools] InvalidNodeClass: class <{}> for module {} is not "
                "a subclass of {}"
                "".format(node_class, module, tooling.CustomToolNode)
            )
            continue

        out[name] = node_class
        logger.debug("[getAllTools] Found [{}]={}".format(name, node_class))

    return out


def getAvailableTools():
    # type: () -> Dict[str, Type[tooling.CustomToolNode]]
    """
    getAllTools() but filtered to remove the tools that have been asked to be ignored
    using an environment variable.
    """
    import os  # defer import to get the latest version of os.environ

    all_tools = getAllTools()

    excluded_tool_var = os.environ.get(c.ENVVAR_EXCLUDED_TOOLS)
    if not excluded_tool_var:
        return all_tools

    for excluded_tool_name in excluded_tool_var.split(os.pathsep):
        if excluded_tool_name in all_tools:
            del all_tools[excluded_tool_name]

    return all_tools


def registerTools():

    global REGISTERED

    if REGISTERED:
        logger.warning("[registerTools] Called but REGISTERED=True. Returning early.")
        return

    for tool_name, tool in getAvailableTools().items():
        NodegraphAPI.RegisterPythonGroupType(tool.name, tool)
        NodegraphAPI.AddNodeFlavor(tool.name, c.FLAVOR_NAME)
        logger.debug("[registerTools] registered ({}){}".format(tool_name, tool))

    REGISTERED = True
    return


def getLayeredMenu():
    # type: () -> LayeredMenuAPI.LayeredMenu

    layeredMenu = LayeredMenuAPI.LayeredMenu(
        _populateCallback,
        _actionCallback,
        keyboardShortcut=c.SHORTCUT,
        alwaysPopulate=False,
        onlyMatchWordStart=False,
        sortAlphabetically=True,
        checkAvailabilityCallback=None,
    )

    logger.debug("[getLayeredMenu] Finished.")
    return layeredMenu


def _populateCallback(layered_menu):
    # type: (LayeredMenuAPI.LayeredMenu) -> None

    available_tools = NodegraphAPI.GetFlavorNodes(c.FLAVOR_NAME, filterExists=True)
    for tool_name in available_tools:  # type: str

        entry_color = tool_name.color or c.COLORS.default

        layered_menu.addEntry(
            tool_name,
            text=tool_name,
            color=entry_color,
        )

    return


def _actionCallback(key):
    # type: (str) -> NodegraphAPI.Node

    available_tools = NodegraphAPI.GetFlavorNodes(c.FLAVOR_NAME, filterExists=True)
    for tool in available_tools:  # type: tooling.CustomToolNode

        if key != tool.name:
            continue

        try:
            node = NodegraphAPI.CreateNode(tool.name, NodegraphAPI.GetRootNode())
        except Exception as excp:
            traceback.print_exc()
            logger.error(
                "[__actionCallback] Error when trying to create node <{}>: {}"
                "".format(tool.name, excp),
            )
            raise
        return node

    return
