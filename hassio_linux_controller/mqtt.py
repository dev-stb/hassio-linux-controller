import paho.mqtt.client as mqtt

import logging

__logger = logging.getLogger(__name__)


class Client(mqtt.Client):

    def __init__(self):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2)
        self._calback_list = {}
        self.on_message = self._on_message

    def _on_message(self, client, userdata, message):
        __logger.info(f"Message received: {message.topic}")
        if message.topic in self._calback_list:
            self._calback_list[message.topic](message.payload)

    def add_callback(self, topic, callback):
        self._calback_list[topic] = callback
