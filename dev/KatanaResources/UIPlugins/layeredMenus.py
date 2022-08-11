import logging
import customtooling.loader

from Katana import LayeredMenuAPI


logger = logging.getLogger(__name__)


def registerLayeredMenus():
    layeredMenu = customtooling.loader.getLayeredMenu()
    LayeredMenuAPI.RegisterLayeredMenu(layeredMenu, "opscripting")
    logger.info(
        "[registerLayeredMenus] Registered <opscripting> with shortcut <{}>"
        "".format(layeredMenu.getKeyboardShortcut())
    )
    return


registerLayeredMenus()
