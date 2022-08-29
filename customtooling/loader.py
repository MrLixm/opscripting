import importlib
import logging
import pkgutil
import sys
from types import ModuleType
from typing import Dict
from typing import Sequence
from typing import Optional
from typing import Type

if sys.version_info[0] == 2:
    from pkgutil import ImpImporter as FileFinder
else:
    from importlib.machinery import FileFinder

from Katana import NodegraphAPI
from Katana import Callbacks
from Katana.Utils import UndoStack

from . import c
from . import nodebase

__all__ = ("registerTools",)

logger = logging.getLogger(__name__)


REGISTERED = {}  # type: Dict[str, Type[nodebase.CustomToolNode]]
"""
Dictionnary of CUstomTool class registered to be used in Katana.
"""


def registerTools(tools_packages_list):
    # type: (Sequence[str]) -> None
    """
    Register the CustomTool declared in the given locations names.
    Those locations must be python package names registered in the PYTHONPATH, so they
    can be converted to modules and imported.

    Must be called once.

    Args:
        tools_packages_list:
            list of python packages name. Those package must be registered in the PYTHONPATH.
    """
    if REGISTERED:
        raise RuntimeError(
            "REGISTERED global is not empty: this means this function has already been"
            "called. You can only call it once."
        )

    NodegraphAPI.RegisterPythonGroupType(c.KATANA_TYPE_NAME, nodebase.CustomToolNode)
    NodegraphAPI.AddNodeFlavor(c.KATANA_TYPE_NAME, "_hide")  # TODO: see if kept
    logger.debug(
        "[registerTools] RegisterPythonGroupType for <{}>".format(c.KATANA_TYPE_NAME)
    )

    for package_id in tools_packages_list:

        try:
            package = importlib.import_module(package_id)  # type: ModuleType
        except Exception as excp:
            logger.exception(
                "[registerTools] Cannot import package <{}>: {}"
                "".format(package_id, excp)
            )
            continue

        registered = _registerToolPackage(package=package)
        # registered tools can be found in REGISTERED global anyway
        continue

    # TO uncomment if needed
    # _registerCallbackCustomTools()

    logger.info(
        "[registerTools] Finished. Registered {} custom tools for {} locations."
        "".format(len(REGISTERED), len(tools_packages_list))
    )
    return


def _createCustomTool(class_name):
    # type: (str) -> NodegraphAPI.Node
    """

    Args:
        class_name: name of the tool to create, must be previously registered.

    Returns:
        Instance of the node created in the Nodegraph.
    """
    custom_tool_class = REGISTERED[class_name]

    UndoStack.DisableCapture()

    try:

        try:
            node = NodegraphAPI.CreateNode("SuperTool")
        except Exception:
            logger.exception(
                '[_createCustomTool] Error creating CustomTool of type "{}"'.format(
                    class_name
                )
            )
            return

        try:

            node.__class__ = custom_tool_class
            node.setType(class_name)
            if not NodegraphAPI.NodegraphGlobals.IsLoading():
                node.setName(class_name)
                node.__init__()

        except Exception:
            logger.exception(
                '[_createCustomTool] Error creating CustomTool of type "{}"'
                "".format(class_name)
            )
            node.delete()
            return

    finally:
        UndoStack.EnableCapture()

    return node


def _registerToolPackage(package):
    # type: (ModuleType) ->  Dict[str, Type[nodebase.CustomToolNode]]
    """

    Args:
        package: python <module> object to import the custom tools from

    Returns:
        all the custom tools loaded as dict[tool_name, tool_class]
    """

    customtool_dict = _getAvailableToolsInPackage(package=package)

    for tool_module_name, tool_class in customtool_dict.items():

        if tool_class.name in REGISTERED:
            logger.warning(
                "[_registerToolPackage] tool from module <{}> from package {} is "
                "already registered as <{}>."
                "".format(tool_module_name, package, tool_class.name)
            )
            continue

        NodegraphAPI.RegisterPythonNodeFactory(tool_class.name, _createCustomTool)
        NodegraphAPI.AddNodeFlavor(tool_class.name, c.KATANA_FLAVOR_NAME)
        REGISTERED[tool_class.name] = tool_class

        logger.debug(
            "[_registerToolPackage] registered ({}){}"
            "".format(tool_module_name, tool_class)
        )
        continue

    logger.debug(
        "[_registerToolPackage] Finished registering package {}, {} tools found."
        "".format(package, len(customtool_dict))
    )
    return customtool_dict


def _getAvailableToolsInPackage(package):
    # type: (ModuleType) -> Dict[str, Type[nodebase.CustomToolNode]]
    """
    _getAllToolsInPackage() but filtered to remove the tools that have been asked to be
    ignored using an environment variable.

    Returns:
        dict of module_name, CustomToolNode class defined in the module
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

    logger.debug(
        "[_getAvailableToolsInPackage] Finished. Excluded {} tools.".format(nexcluded)
    )
    return all_tools


def _getAllToolsInPackage(package):
    # type: (ModuleType) -> Dict[str, Type[nodebase.CustomToolNode]]
    """
    Get a list of all the "tools" modules available in the given package.

    Not recommended to use as the "final" function. See ``getAvailableTools()`` instead.

    SRC: https://stackoverflow.com/a/1310912/13806195

    Returns:
        dict of module_name, CustomToolNode class defined in the module
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

        if name.startswith("_"):
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

        try:
            node_class._check()
        except AssertionError as excp:
            logger.exception(
                "[getAllToolsInPackage] InvalidNodeClass: class <{}> for module {}:\n"
                "   {}".format(node_class, module, excp)
            )
            continue

        out[name] = node_class
        logger.debug("[_getAllToolsInPackage] Found [{}]={}".format(name, node_class))

    return out


def _registerCallbackCustomTools():
    """
    Add a new callback when a node is created in the Nodegraph to apply additional
    operations on a CustomToolNode.

    .. this is not called by default. Up to the developer to enable it.
    """
    Callbacks.addCallback(
        Callbacks.Type.onNodeCreate,
        nodebase.customToolNodeCallback,
    )
    logger.debug("[_registerCallbackCustomTools] added callback onNodeCreate")
    return
