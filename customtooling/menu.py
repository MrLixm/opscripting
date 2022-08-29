import logging

from Katana import NodegraphAPI
from Katana import LayeredMenuAPI
from Katana import Utils

from . import c


__all__ = ("getLayeredMenuForAllCustomTool",)

logger = logging.getLogger(__name__)


def getLayeredMenuForAllCustomTool():
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

    available_tools = NodegraphAPI.GetFlavorNodes(
        c.KATANA_FLAVOR_NAME, filterExists=True
    )
    for tool_name in available_tools:  # type: str

        # HACK: to quickly be able to access the CustomTool class for this nodeType
        # TODO: this involve a time penalty the first time the menu is created
        # It can become problematic when here is a lot of node.
        try:
            node = NodegraphAPI.CreateNode(tool_name, NodegraphAPI.GetRootNode())
            Utils.EventModule.ProcessEvents()
            entry_color = node.color or c.COLORS.default

        except Exception as excp:
            node = None
            entry_color = c.COLORS.default
            logger.warning(
                "[_populateCallback] Can't create node for tool <{}>: {}\n"
                "   layeredMenu Entry still created".format(tool_name, excp)
            )

        layered_menu.addEntry(
            tool_name,
            text=tool_name,
            color=entry_color,
        )

        if node:
            node.delete()
            Utils.EventModule.ProcessEvents()

        continue

    return


def _actionCallback(key):
    # type: (str) -> NodegraphAPI.Node

    available_tools = NodegraphAPI.GetFlavorNodes(
        c.KATANA_FLAVOR_NAME, filterExists=True
    )
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
