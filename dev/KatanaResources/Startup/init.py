"""
Executed when Katana starts.
"""
import logging

from Katana import Callbacks

logger = logging.getLogger(__name__)


def onStartupComplete(objectHash):

    from opscripttools.loader import registerTools

    registerTools()
    return


logger.info("Registering onStartupComplete callback...")
Callbacks.addCallback(Callbacks.Type.onStartupComplete, onStartupComplete)
