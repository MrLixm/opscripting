import importlib
import logging
import pkgutil
import sys
from typing import Dict
from typing import Iterable
from types import ModuleType
from typing import Optional
from typing import Type

if sys.version_info[0] == 2:
    from pkgutil import ImpImporter as FileFinder
else:
    from importlib.machinery import FileFinder

from Katana import NodegraphAPI

from . import c
from . import nodebase

__all__ = ("registerTools",)

logger = logging.getLogger(__name__)


def registerTools(tools_packages_list):
    # type: (Iterable[str]) -> None
    """
    Register the CustomTool declared in the given locations names.
    Those locations must be python package names registered in the PYTHONPATH, so they
    can be converted to modules and imported.

    Args:
        tools_packages_list:
            list of python packages name. Those package must be registered in the PYTHONPATH.
    """

    for package_id in tools_packages_list:

        try:
            package = importlib.import_module(package_id)  # type: ModuleType
        except Exception as excp:
            logger.exception(
                "[registerTools] Cannot import package <{}>: {}"
                "".format(package_id, excp)
            )
            continue

        _registerToolPackage(package=package)

    return


def _registerToolPackage(package):
    # type: (ModuleType) -> None

    customtool_list = _getAvailableTools(package=package)

    for tool_name, tool in customtool_list.items():

        NodegraphAPI.RegisterPythonGroupType(tool.name, tool)
        NodegraphAPI.AddNodeFlavor(tool.name, c.FLAVOR_NAME)

        logger.debug("[registerTools] registered ({}){}".format(tool_name, tool))
        continue

    logger.debug(
        "[registerTools] Finished registering {}, {} tools found."
        "".format(package, len(customtool_list))
    )
    return


def _getAvailableTools(package):
    # type: (ModuleType) -> Dict[str, Type[nodebase.CustomToolNode]]
    """
    getAllTools() but filtered to remove the tools that have been asked to be ignored
    using an environment variable.
    """
    import os  # defer import to get the latest version of os.environ

    all_tools = _getAllToolsInPackage(package)

    excluded_tool_var = os.environ.get(c.ENVVAR_EXCLUDED_TOOLS)
    if not excluded_tool_var:
        return all_tools

    tools_to_exclude = excluded_tool_var.split(os.pathsep)
    nexcluded = 0
    for excluded_tool_name in tools_to_exclude:
        if excluded_tool_name in all_tools:
            del all_tools[excluded_tool_name]
            nexcluded += 1

    logger.debug("[getAvailableTools] Finished. Excluded {} tools.".format(nexcluded))
    return all_tools


def _getAllToolsInPackage(package):
    # type: (ModuleType) -> Dict[str, Type[nodebase.CustomToolNode]]
    """
    Get a list of all the "tools" modules available in the given package.

    Not recommended to use as the "final" function. See ``getAvailableTools()`` instead.

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
                "[getAllToolsInPackage][loadModule] Cannot load <{}>: {}"
                "".format(module_name_, excp)
            )
            return

        return module_

    import os  # defer import to get the latest version of os.environ

    out = dict()
    pkgpath = os.path.dirname(package.__file__)

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
                "[getAllToolsInPackage] tool module <{}> doesn't declare the "
                "NODE variable.".format(name)
            )
            continue

        if not issubclass(node_class, nodebase.CustomToolNode):
            logger.error(
                "[getAllToolsInPackage] InvalidNodeClass: class <{}> for module {} "
                "is not a subclass of {}"
                "".format(node_class, module, nodebase.CustomToolNode)
            )
            continue

        out[name] = node_class
        logger.debug("[getAllToolsInPackage] Found [{}]={}".format(name, node_class))

    return out
