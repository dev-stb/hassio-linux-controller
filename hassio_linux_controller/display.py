import os
import logging


import hassio_linux_controller.env as env
import hassio_linux_controller.api as api

_logger = logging.getLogger(__name__)


def on():
    _logger.info("Display on")
    if not env.dry_run:
        os.system(f"xset -display {env.display} dpms force on")


def off():
    _logger.info("Display off")
    if not env.dry_run:
        os.system(f"xset -display {env.display} dpms force off")


def loop_step():
    if api.get_status_of_switch(env.display_entitiy_id):
        on()
    else:
        off()
