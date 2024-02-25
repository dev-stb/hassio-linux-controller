import paho.mqtt.client as mqtt

import logging

__logger = logging.getLogger(__name__)


@staticmethod
def _on_message(client, userdata, message):
    __logger.info(f"Message received: {message.topic}")
    if message.topic in client._calback_list:
        client._calback_list[message.topic]()


class MagicMirrorClient(mqtt.Client):

    def __init__(self):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2, "MagicMirror")
        self._calback_list = {}
        self.on_message = _on_message

    def add_callback(self, topic, callback):
        self._calback_list[topic] = callback
        self.subscribe(topic)
