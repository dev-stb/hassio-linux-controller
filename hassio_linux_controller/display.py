import os
import logging
import time
 import subprocess

import hassio_linux_controller.env as env
import hassio_linux_controller.api as api

_logger = logging.getLogger(__name__)

__log_state = 0


def set_to(on:bool):
    global __log_state
    global _logger
    if __log_state == 0:
        _logger.info(f"Display {'on' if on else 'off'}")
        __log_state = 1
    if not env.config.dry_run:
        subprocess = subprocess.Popen(
            f"xset -display {env.config.display} dpms force {'on' if on else 'off'}"
            stdout=subprocess.STDOUT,
            stderr=subprocess.STDOUT,
            env={"DISPLAY": env.config.display},
        )
        time.sleep(0.1)
        exit_code = subprocess.poll()

        if exit_code != 0:
            _logger.error(f"Display {'on' if on else 'off'} failed with exit code {exit_code}")


def loop_step():
    if api.get_status_of_switch(env.config.display_entity_id):
        set_to(True)
    else:
        set_to(False)
