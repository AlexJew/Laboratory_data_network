import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, reasonCode, properties):
    print("Connected with result code:", reasonCode)

NAME = 'className'
HOST = '192.168.0.199'
PORT = 1883
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(HOST, PORT, 60)
client.loop_start() 