import logging
import urllib.parse
import requests

import hassio_linux_controller.env as env
from .models import HassioError

_logger = logging.getLogger(__name__)


def get_status_of_switch(entity_id: str) -> bool:
    _logger.debug(
        f"Checking status of {entity_id} in hassio: {env.config.url}",
    )
    response = requests.get(
        urllib.parse.urljoin(
            env.config.url,
            f"api/states/{entity_id}",
        ),
        headers=env.config.headers,
    )
    _logger.debug(
        f"Response: {response.status_code} {response.reason}",
    )
    if response.status_code != 200:
        raise HassioError(
            response.status_code,
            f"Error: {response.status_code} {response.reason}",
        )
    response_json = response.json()
    return response_json["state"] == "on"


def set_status_of_switch(entity_id: str, value: bool) -> None:
    _logger.debug(
        f"Set status of {entity_id} in hassio: {env.config.url}",
    )
    response = requests.post(
        urllib.parse.urljoin(
            env.config.url,
            f"api/states/{entity_id}",
        ),
        headers=env.config.headers,
        json={"state": "on" if value else "off"},
    )
    _logger.debug(
        f"Response: {response.status_code} {response.reason}",
    )
    if response.status_code != 200:
        raise HassioError(
            response.status_code,
            f"Error: {response.status_code} {response.reason}",
        )
