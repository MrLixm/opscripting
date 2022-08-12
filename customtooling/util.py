import logging

__all__ = ("asserting",)

logger = logging.getLogger(__name__)


def asserting(expression, msg):
    # type: (bool, str) -> None
    """
    It is not recommended to use ``assert`` in CustomTool as the error will not be
    raised in the log. Instead we can use this shortand function that will actually log.

    Args:
        expression: object that must be asserted to true
        msg: message to display in the exception

    Returns:

    """
    if not expression:
        logger.error(msg)
        raise AssertionError(msg)
