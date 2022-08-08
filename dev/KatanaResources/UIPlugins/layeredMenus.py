import logging
import opscripttools.integrating

from Katana import LayeredMenuAPI


logger = logging.getLogger(__name__)


def registerLayeredMenus():
    layeredMenu = opscripttools.integrating.getLayeredMenu()
    LayeredMenuAPI.RegisterLayeredMenu(layeredMenu, "opscripting")
    logger.info(
        "[registerLayeredMenus] Registered <opscripting> with shortcut <{}>"
        "".format(layeredMenu.getKeyboardShortcut())
    )
    return


registerLayeredMenus()
