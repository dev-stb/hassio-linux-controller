import sys
import logging

from hassio_linux_controller import env

env.load()
logging.basicConfig(
    stream=sys.stdout,
    level=env.config.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
_logger = logging.getLogger(__name__)
env.print_config()

from hassio_linux_controller import mqtt, power, firefox, display


mqttc = mqtt.MagicMirrorClient()


def register(
    client: mqtt.MagicMirrorClient, userdata, flags, reason_code, properties
):
    _logger.info(
        f"Register @ mqtt {reason_code=} {properties=} {userdata=} {flags=}"
    )
    if reason_code.is_failure:
        _logger.error(f"Failed to register @ mqtt {reason_code=}")
        return
    _logger.info("Register @ mqtt done")
    display.register(client)
    firefox.register(client)
    power.register(client)


mqttc.on_connect = register
mqttc.connect(
    env.config.mqtt_url,
    env.config.mqtt_port,
    env.config.mqtt_keepalive,
)
mqttc.username_pw_set(
    env.config.mqtt_username,
    env.config.mqtt_password,
)
mqttc.on_log = lambda client, userdata, level, buf: _logger.info(buf)

try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    pass
