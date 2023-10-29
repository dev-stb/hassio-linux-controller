import os
import argparse
from pydantic import BaseModel

# is set later after logging is initialized
_logger = None


class Configuration(BaseModel):
    log_level: str
    url: str
    token: str
    interval_s: int
    display: str
    display_entity_id: str
    invoke_shutdown_entity_id: str
    invoke_reboot_entity_id: str
    start_kioskmode_firefox_entity_id: str
    dry_run: bool

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
        "--interval-s",
        type=int,
        default=_get_int_config("INTERVAL_S", 1),
        help="Interval in seconds",
    )
    parser.add_argument(
        "--display",
        type=str,
        default=_get_str_config("DISPLAY_ID", ":0"),
        help="Display ID",
    )
    parser.add_argument(
        "--display-entity-id",
        type=str,
        default=_get_str_config("DISPLAY_ENTITY_ID", ""),
        help="Display entity ID",
    )
    parser.add_argument(
        "--invoke-shutdown-entity-id",
        type=str,
        default=_get_str_config("INVOKE_SHUTDOWN_ENTITY_ID", ""),
        help="Invoke shutdown entity ID",
    )
    parser.add_argument(
        "--invoke-reboot-entity-id",
        type=str,
        default=_get_str_config("INVOKE_REBOOT_ENTITY_ID", ""),
        help="Invoke reboot entity ID",
    )
    parser.add_argument(
        "--start-kioskmode-firefox-entity-id",
        type=str,
        default=_get_str_config("START_KIOSKMODE_FIREFOX_ENTITY_ID", ""),
        help="Start kioskmode firefox entity ID",
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


def _get_str_config(key: str, default: str = "") -> str:
    value = default
    env_value = os.environ.get(
        f"HASSIO_LINUX_CONTROLLER_{key}",
        None,
    )
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
