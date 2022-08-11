import logging

from Katana import NodegraphAPI
from Katana import LayeredMenuAPI

from . import c


__all__ = ("getLayeredMenuForAllCUstomTool",)

logger = logging.getLogger(__name__)


def getLayeredMenuForAllCUstomTool():
    # type: () -> LayeredMenuAPI.LayeredMenu

    layeredMenu = LayeredMenuAPI.LayeredMenu(
        _populateCallback,
        _actionCallback,
        keyboardShortcut=c.LAYEREDMENU_SHORTCUT,
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

        # TODO: find a way to convet the tool_name to the tool's Class
        entry_color = c.COLORS.default

        layered_menu.addEntry(
            tool_name,
            text=tool_name,
            color=entry_color,
        )

    return


def _actionCallback(key):
    # type: (str) -> NodegraphAPI.Node

    available_tools = NodegraphAPI.GetFlavorNodes(c.FLAVOR_NAME, filterExists=True)
    for tool_name in available_tools:  # type: str

        if key != tool_name:
            continue

        try:
            node = NodegraphAPI.CreateNode(tool_name, NodegraphAPI.GetRootNode())
        except Exception as excp:
            logger.error(
                "[__actionCallback] Error when trying to create node <{}>: {}"
                "".format(tool_name, excp),
            )
            raise

        if node is None:
            logger.error(
                "[_actionCallback] CreateNode({}) returned None. This might comes "
                "from any error in the class registered for this tool so check the "
                "code.".format(key)
            )

        return node

    return
