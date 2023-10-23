import sys
import time
import logging

import hassio_linux_controller.env as env
from .models import HassioError

import hassio_linux_controller.display as display
import hassio_linux_controller.power as power

logging.basicConfig(stream=sys.stdout, level=env.log_level)
_logger = logging.getLogger(__name__)


def main():
    try:
        display.loop_step()
        while True:
            try:
                time.sleep(env.interval_s)
                display.loop_step()
                power.loop_step()
            except HassioError as e:
                _logger.exception(e)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
