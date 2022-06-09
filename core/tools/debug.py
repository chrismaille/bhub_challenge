from asbool import asbool
from stela import settings


def show_toolbar(_) -> bool:
    """Show Django Debug Toolbar.

    Original code: debug_toolbar.middleware.show_toolbar

    :return: boolean
    """

    return asbool(settings["project.show_debug_toolbar"]) and asbool(
        settings["project.debug"],
    )
