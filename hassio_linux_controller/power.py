import os
import logging

from hassio_linux_controller import env, mqtt, display

_logger = logging.getLogger(__name__)


def _shutdown():
    _logger.info("Invoke shutdown")
    if not env.config.dry_run:
        exit_code = os.system("shutdown -h +1")
    if exit_code != 0:
        _logger.error(f"Shutdown failed with exit code {exit_code}")
    if exit_code == 0:
        display.off()


def _reboot():
    _logger.info("Invoke reboot")
    if not env.config.dry_run:
        exit_code = os.system("shutdown --reboot +1")
    if exit_code != 0:
        _logger.error(f"Reboot failed with exit code {exit_code}")


def register(client: mqtt.MagicMirrorClient):
    client.add_callback("hassio/power/shutdown", _shutdown)
    client.add_callback("hassio/power/reboot", _reboot)
