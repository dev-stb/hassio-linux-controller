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
    set_str = "auto" if on else "off"
    if __log_state != on:
        _logger.info(f"Display {set_str}")
        __log_state = on
        if not env.config.dry_run:
            process = subprocess.run(
                f"xrandr --display '{env.config.display}' --output HDMI-1 --{set_str} --rotate left",
                shell=True,
                text=True,
                capture_output=True,
            )
            if process.stdout:
                _logger.warn(process.stdout)
            if process.stderr:
                _logger.error(process.stderr)
            if process.returncode != 0:
                _logger.error(
                    f"Display {set_str} failed with exit code {process.returncode}"
                )


def loop_step():
    if api.get_status_of_switch(env.config.display_entity_id):
        set_to(True)
    else:
        set_to(False)
