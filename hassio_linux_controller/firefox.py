import subprocess
import logging


from hassio_linux_controller import env, mqtt

_logger = logging.getLogger(__name__)

__subprocess = None


def open_process():
    global __subprocess
    _logger.info("Firefox (re-)open process")
    __subprocess = subprocess.Popen(
        " ".join(
            [
                "firefox",
                "--display",
                f"'{env.config.display}'",
                "--kiosk",
                # "--marionette",
                "'http://home/lovelace-magicmirror/0?BrowserID=MagicMirror'",
            ]
        ),
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def check_process():
    global __subprocess
    if not env.config.dry_run:
        if __subprocess is None:
            open_process()
        else:
            exit_code = __subprocess.returncode
            if exit_code is not None:
                _logger.error(
                    f"Firefox process exited with exit code {exit_code}"
                )
                open_process()


def kill_process():
    global __subprocess
    if __subprocess is not None:
        _logger.info("Firefox kill process")
        if not env.config.dry_run:
            warn = __subprocess.stdout.readlines()
            if warn:
                _logger.warn(warn)
            errors = __subprocess.stderr.readlines()
            if errors:
                _logger.error(errors)
            __subprocess.kill()
        __subprocess = None


def register(client: mqtt.Client):
    client.add_callback("hassio/firefox/kill", kill_process)
    client.add_callback("hassio/firefox/open", check_process)
