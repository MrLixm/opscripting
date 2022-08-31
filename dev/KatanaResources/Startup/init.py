"""
Executed when Katana starts.
"""
import logging

from Katana import Callbacks

logger = logging.getLogger(__name__)


def onStartupComplete(objectHash):

    from customtooling.loader import registerTools
    from customtooling.loader import registerCallbacks

    # make sure "opscriptlibrary" parent dir is in the PYTHONPATH
    locations_to_register = ("opscriptlibrary",)

    registerTools(locations_to_register)
    registerCallbacks()
    return


logger.info("Registering onStartupComplete callback...")
Callbacks.addCallback(Callbacks.Type.onStartupComplete, onStartupComplete)
