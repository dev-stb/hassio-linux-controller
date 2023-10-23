import os
import logging


import hassio_linux_controller.env as env
import hassio_linux_controller.api as api
import hassio_linux_controller.display as display

_logger = logging.getLogger(__name__)


def loop_step():
    exit_code = None
    if api.get_status_of_switch(env.invoke_shutdown_entitiy_id):
        _logger.info("Invoke shutdown")
        if not env.dry_run:
            exit_code = os.system("shutdown -h +1")
        if exit_code != 0:
            _logger.error(f"Shutdown failed with exit code {exit_code}")
        api.set_status_of_switch(env.invoke_shutdown_entitiy_id, False)
        if exit_code == 0:
            display.off()
    elif api.get_status_of_switch(env.invoke_reboot_entitiy_id):
        _logger.info("Invoke reboot")
        if not env.dry_run:
            exit_code = os.system("shutdown --reboot +1")
        if exit_code != 0:
            _logger.error(f"Reboot failed with exit code {exit_code}")
        api.set_status_of_switch(env.invoke_reboot_entitiy_id, False)
