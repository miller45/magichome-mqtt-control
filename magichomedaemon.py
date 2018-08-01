import paho.mqtt.client as mqtt
import json
import ledcodes


class MagicHomeDaemon:
    DC = 23

    def __init__(self):
        self.mqtturl = "192.168.0.18"
        self.ledcodes = ledcodes.LedCodes()

        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))

            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("tele/sonoff/LS01/#")
            client.subscribe("stat/sonoff/LS01/#")

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            if not (msg is None and msg.topic is None):
                if msg.topic.startswith("tele"):
                    self.process_tele(msg.topic, msg.payload)
                if msg.topic.startswith("stat"):
                    self.process_stat(msg.topic, msg.payload)

        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message

    def ping(self):
        print("ping from magichomedaem")

    def process_tele(self, topic, msg):
        if topic.endswith("/RESULT"):
            ir = json.loads(msg)
            if not (ir["IrReceived"] is None):
                data = ir["IrReceived"]["Data"]
                if data == self.ledcodes.LE_ON:
                    self.client.publish("cmnd/sonoff/LS01/Dimmer", "100")

                if data == self.ledcodes.LE_OFF:
                    self.client.publish("cmnd/sonoff/LS01/Dimmer", "0")

                if data == self.ledcodes.LE_W:
                    self.client.publish("cmnd/sonoff/LS01/Color", "12")

                if data == self.ledcodes.LE_R1:
                    self.client.publish("cmnd/sonoff/LS01/Color", "1")

                if data == self.ledcodes.LE_G1:
                    self.client.publish("cmnd/sonoff/LS01/Color", "2")

                if data == self.ledcodes.LE_B1:
                    self.client.publish("cmnd/sonoff/LS01/Color", "3")

                if data == self.ledcodes.LE_BRIGHTER:
                    self.client.publish("cmnd/sonoff/LS01/Dimmer", "+")

                if data == self.ledcodes.LE_DIMMER:
                    self.client.publish("cmnd/sonoff/LS01/Dimmer", "-")
        print(msg)

    def process_stat(self, topic, msg):
        print(topic)

    def loop_forever(self):

        self.client.connect(self.mqtturl, 1883, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_forever()
