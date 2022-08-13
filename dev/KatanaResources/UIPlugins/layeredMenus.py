import logging
import customtooling.menu

from Katana import LayeredMenuAPI


logger = logging.getLogger(__name__)


def registerLayeredMenus():

    layered_menu_name = "customtooling"

    layered_menu = customtooling.menu.getLayeredMenuForAllCustomTool()
    LayeredMenuAPI.RegisterLayeredMenu(layered_menu, layered_menu_name)
    logger.info(
        "[registerLayeredMenus] Registered <{}> with shortcut <{}>"
        "".format(layered_menu_name, layered_menu.getKeyboardShortcut())
    )
    return


registerLayeredMenus()
