import subprocess
import logging


import hassio_linux_controller.env as env
import hassio_linux_controller.api as api

_logger = logging.getLogger(__name__)

__subprocess = None


def open_process():
    global __subprocess
    _logger.info("Firefox (re-)open process")
    __subprocess = subprocess.Popen(
        'DISPLAY=:0 firefox --kiosk --marionette "http://home/lovelace-magicmirror/0?wp_enabled=true&&BrowserID=MagicMirror"',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def check_process():
    if not env.dry_run:
        global __subprocess
        if __subprocess is None or __subprocess.poll() is not None:
            open_process()


def kill_process():
    _logger.info("Firefox kill process")
    if not env.dry_run:
        global __subprocess
        if __subprocess is not None:
            __subprocess.kill()
            __subprocess = None


def loop_step():
    if api.get_status_of_switch(env.start_kioskmode_firefox_entity_id):
        check_process()
    else:
        kill_process()
