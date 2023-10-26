import os
import logging


import hassio_linux_controller.env as env
import hassio_linux_controller.api as api

_logger = logging.getLogger(__name__)


def on():
    _logger.info("Display on")
    if not env.config.dry_run:
        os.system(f"xset -display {env.config.display} dpms force on")


def off():
    _logger.info("Display off")
    if not env.config.dry_run:
        os.system(f"xset -display {env.config.display} dpms force off")


def loop_step():
    if api.get_status_of_switch(env.config.display_entity_id):
        on()
    else:
        off()
