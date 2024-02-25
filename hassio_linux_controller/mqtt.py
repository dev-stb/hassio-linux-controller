import paho.mqtt.client as mqtt


import hassio_linux_controller.display as display
import hassio_linux_controller.power as power
import hassio_linux_controller.firefox as firefox


class Client(mqtt.Client):

    def __init__(self):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2)
        self._calback_list = {}
        self.on_connect = self.register
        self.on_message = self._on_message

    def _on_message(self, client, userdata, message):
        if message.topic in self._calback_list:
            self._calback_list[message.topic](message.payload)

    def add_callback(self, topic, callback):
        self._calback_list[topic] = callback

    def register(self):
        display.register(self)
        firefox.register(self)
        power.register(self)
