import logging
import os
import pkgutil
import sys
import traceback
from types import ModuleType
from typing import Dict

if sys.version_info[0] == 2:
    from pkgutil import ImpImporter as FileFinder
else:
    from importlib.machinery import FileFinder

from Katana import NodegraphAPI
from Katana import LayeredMenuAPI

from . import tools
from . import c

__all__ = (
    "getAllTools",
    "getAvailableTools",
    "getLayeredMenu",
)

logger = logging.getLogger(__name__)


def getAllTools():
    # type: () -> Dict[str, ModuleType]
    """
    Get a list of all the "tools" modules available.

    SRC: https://stackoverflow.com/a/1310912/13806195
    """
    pkgpath = os.path.dirname(tools.__file__)
    out = dict()
    for module_loader, name, ispkg in pkgutil.iter_modules([pkgpath]):
        if ispkg:  # tools can only be modules
            continue
        out[name] = _loadModule(module_loader, name)

    return out


def getAvailableTools():
    # type: () -> Dict[str, ModuleType]
    """
    getAllTools() but filtered to remove the tools that have been asked to be ignored.
    """
    all_tools = getAllTools()

    excluded_tool_var = os.environ.get(c.ENVVAR_EXCLUDED_TOOLS)
    if not excluded_tool_var:
        return all_tools

    for excluded_tool in excluded_tool_var.split(os.pathsep):
        if excluded_tool in all_tools:
            del all_tools[excluded_tool]

    return all_tools


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

    all_tools = getAvailableTools()
    logger.debug(
        "[getLayeredMenu] Created menu for {} tools : {}"
        "".format(len(all_tools), all_tools)
    )

    return layeredMenu


def _loadModule(module_loader, module_name):
    # type: (FileFinder, str) -> ModuleType
    """
    Python 2 and 3 compatible.
    """
    module = module_loader.find_module(module_name).load_module(module_name)
    return module


def _populateCallback(layered_menu):
    # type: (LayeredMenuAPI.LayeredMenu) -> None

    for module_name, module in getAvailableTools().items():

        entry_name = module_name.title()
        try:
            entry_color = module.COLOR
        except Exception:
            entry_color = c.COLORS.default

        layered_menu.addEntry(
            module_name,
            text=entry_name,
            color=entry_color,
        )

    return


def _actionCallback(key):
    # type: (str) -> NodegraphAPI.Node

    for module_name, module in getAvailableTools().items():

        if key != module_name:
            continue

        try:
            node = module.build()
        except Exception as excp:
            traceback.print_exc()
            logger.error(
                "[__actionCallback] Error when trying to call build() on module <{}>"
                "".format(module_name),
            )
            raise
        return node

    return
