import os
import logging


import hassio_linux_controller.env as env
import hassio_linux_controller.api as api
import hassio_linux_controller.display as display

_logger = logging.getLogger(__name__)

__sleep_factor = 60 / env.config.interval_s
__sleep_counter = 0


def loop_step():
    global __sleep_counter
    global __sleep_factor
    if __sleep_counter < __sleep_factor:
        __sleep_counter += 1
        return
    __sleep_counter = 0

    exit_code = None
    if api.get_status_of_switch(env.config.invoke_shutdown_entity_id):
        _logger.info("Invoke shutdown")
        if not env.config.dry_run:
            exit_code = os.system("shutdown -h +1")
        if exit_code != 0:
            _logger.error(f"Shutdown failed with exit code {exit_code}")
        api.set_status_of_switch(env.config.invoke_shutdown_entity_id, False)
        if exit_code == 0:
            display.off()
    elif api.get_status_of_switch(env.config.invoke_reboot_entity_id):
        _logger.info("Invoke reboot")
        if not env.config.dry_run:
            exit_code = os.system("shutdown --reboot +1")
        if exit_code != 0:
            _logger.error(f"Reboot failed with exit code {exit_code}")
        api.set_status_of_switch(env.config.invoke_reboot_entity_id, False)
