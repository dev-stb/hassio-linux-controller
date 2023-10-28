import sys
import time
import logging

import hassio_linux_controller.env as env
from .models import HassioError


def main():
    try:
        env.load()
        logging.basicConfig(
            stream=sys.stdout,
            level=env.config.log_level,
            format="%(asctime)s %(levelname)s %(name)s %(message)s",
        )
        _logger = logging.getLogger(__name__)
        env.print_config()

        import hassio_linux_controller.display as display
        import hassio_linux_controller.power as power
        import hassio_linux_controller.firefox as firefox

        display.loop_step()
        firefox.loop_step()
        while True:
            try:
                time.sleep(env.config.interval_s)
                display.loop_step()
                power.loop_step()
                firefox.loop_step()
            except HassioError as e:
                _logger.exception(e)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
