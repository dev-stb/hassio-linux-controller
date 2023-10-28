import os
import logging
import time
import subprocess

import hassio_linux_controller.env as env
import hassio_linux_controller.api as api

_logger = logging.getLogger(__name__)

__log_state = 0


def set_to(on: bool):
    global __log_state
    global _logger
    set_str = "on" if on else "off"
    if __log_state != on:
        _logger.info(f"Display {set_str}")
        __log_state = on
    if not env.config.dry_run:
        process = subprocess.Popen(
            f"xset -display '{env.config.display}' dpms force {set_str}",
        )
        time.sleep(0.1)
        exit_code = process.poll()

        _logger.info(process.stdout.read())
        _logger.info(process.stderr.read())

        if exit_code != 0:
            _logger.error(
                f"Display {set_str} failed with exit code {exit_code}"
            )


def loop_step():
    if api.get_status_of_switch(env.config.display_entity_id):
        set_to(True)
    else:
        set_to(False)
