import os
import logging


import hassio_linux_controller.env as env
import hassio_linux_controller.api as api

_logger = logging.getLogger(__name__)

__log_state = 0


def on():
    global __log_state
    global _logger
    if __log_state == 0:
        _logger.info("Display on")
        __log_state = 1
    if not env.config.dry_run:
        exit_code = os.system(
            f"xset -display {env.config.display} dpms force on"
        )
        if exit_code != 0:
            _logger.error(f"Display on failed with exit code {exit_code}")


def off():
    global __log_state
    global _logger
    if __log_state == 1:
        _logger.info("Display off")
        __log_state = 0
    if not env.config.dry_run:
        exit_code = os.system(
            f"xset -display {env.config.display} dpms force off"
        )
        if exit_code != 0:
            _logger.error(f"Display off failed with exit code {exit_code}")


def loop_step():
    if api.get_status_of_switch(env.config.display_entity_id):
        on()
    else:
        off()
