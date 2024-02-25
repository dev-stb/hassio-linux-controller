import os
import argparse
from pydantic import BaseModel

# is set later after logging is initialized
_logger = None


class Configuration(BaseModel):
    log_level: str
    url: str
    token: str
    display: str
    dry_run: bool

    mqtt_url: str = "localhost"
    mqtt_port: int = 1883
    mqtt_keepalive: int = 60
    mqtt_username: str = ""
    mqtt_password: str = ""

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {config.token}",
            "content_type": "application/json",
        }


config: Configuration = None


def load() -> None:
    global config

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level",
        type=str,
        default=_get_str_config("LOG_LEVEL", "INFO"),
        help="Log level",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=_get_str_config("HASSIO_URL", "http://localhost:8123"),
        help="Hassio URL",
    )
    parser.add_argument(
        "--token",
        type=str,
        default=_get_str_config(
            "HASSIO_BEARER_TOKEN", "<please set this token>"
        ),
        help="Hassio bearer token",
    )
    parser.add_argument(
        "--display",
        type=str,
        default=_get_str_config("DISPLAY", ":0", use_app_prefix=False),
        help="Display ID",
    )
    parser.add_argument(
        "--mqtt-url",
        type=str,
        default=_get_str_config("MQTT_URL", "localhost"),
        help="MQTT URL",
    )
    parser.add_argument(
        "--mqtt-port",
        type=int,
        default=_get_int_config("MQTT_PORT", 1883),
        help="MQTT port",
    )
    parser.add_argument(
        "--mqtt-keepalive",
        type=int,
        default=_get_int_config("MQTT_KEEPALIVE", 60),
        help="MQTT keepalive",
    )
    parser.add_argument(
        "--mqtt-username",
        type=str,
        default=_get_str_config("MQTT_USERNAME", ""),
        help="MQTT username",
    )
    parser.add_argument(
        "--mqtt-password",
        type=str,
        default=_get_str_config("MQTT_PASSWORD", ""),
        help="MQTT password",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=_get_bool_config("DRY_RUN", False),
        help="Dry run",
    )

    args = parser.parse_args()

    config = Configuration.model_validate(args.__dict__)


def print_config() -> None:
    global config
    global _logger
    if _logger is None:
        import logging

        _logger = logging.getLogger(__name__)

    _logger.info(f"Configuration: {config=}")


def _get_str_config(
    key: str,
    default: str = "",
    use_app_prefix: bool = True,
) -> str:
    value = default
    env_key = key
    if use_app_prefix:
        env_key = f"HASSIO_LINUX_CONTROLLER_{key}"

    env_value = os.environ.get(env_key, None)
    if env_value is not None:
        value = env_value

    return value


def _get_bool_config(key: str, default: bool) -> bool:
    return _get_str_config(key, str(default)).lower() in [
        "1",
        "t",
        "y",
        "on",
        "yes",
        "true",
    ]


def _get_int_config(key: str, default: int) -> int:
    value = _get_str_config(key, str(default))
    return int(value)
