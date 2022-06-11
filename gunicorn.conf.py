from asbool import asbool
from loguru import logger

from core.services.sentry import configure_sentry

configure_sentry()
from stela import settings  # noqa

logger.info(f"Configuring gunicorn... Environment is: {settings['ENV']}")

bind: str = "0.0.0.0:8080"
# All A55 projects are currently running in the same machine.
workers: int = 2
log_level: str = "debug"
timeout: int = 30 if asbool(settings["project.reload_app"]) else 120
reload: bool = asbool(settings["project.reload_app"])
reload_engine: str = "poll"
preload_app: bool = not reload
error_log = "-"
access_log = "-"
