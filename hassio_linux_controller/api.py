import logging
import urllib.parse
import requests

import hassio_linux_controller.env as env
from .models import HassioError

_logger = logging.getLogger(__name__)


def get_status_of_switch(entitiy_id: str) -> bool:
    _logger.debug(
        f"Checking status of {entitiy_id} in hassio: {env.url}",
    )
    response = requests.get(
        urllib.parse.urljoin(
            env.url,
            f"api/states/{entitiy_id}",
        ),
        headers=env.headers,
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


def set_status_of_switch(entitiy_id: str, value: bool) -> None:
    _logger.debug(
        f"Set status of {entitiy_id} in hassio: {env.url}",
    )
    response = requests.post(
        urllib.parse.urljoin(
            env.url,
            f"api/states/{entitiy_id}",
        ),
        headers=env.headers,
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
