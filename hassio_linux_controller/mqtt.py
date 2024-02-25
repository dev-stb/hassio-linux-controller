import paho.mqtt.client as mqtt


class Client(mqtt.Client):

    def __init__(self):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2)
        self._calback_list = {}
        self.on_message = self._on_message

    def _on_message(self, client, userdata, message):
        if message.topic in self._calback_list:
            self._calback_list[message.topic](message.payload)

    def add_callback(self, topic, callback):
        self._calback_list[topic] = callback
