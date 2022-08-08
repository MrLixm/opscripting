import logging
import opscripting.integrating

from Katana import LayeredMenuAPI


logger = logging.getLogger(__name__)


def registerLayeredMenus():
    layeredMenu = opscripting.integrating.getLayeredMenu()
    LayeredMenuAPI.RegisterLayeredMenu(layeredMenu, "opscripting")
    logger.info(
        "[registerLayeredMenus] Registered <opscripting> with shortcut <{}>"
        "".format(layeredMenu.getKeyboardShortcut())
    )
    return


registerLayeredMenus()
