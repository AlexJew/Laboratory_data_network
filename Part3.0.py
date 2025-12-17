import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connecté avec le code de retour :", rc)
    client.subscribe("smartplug/relay/set")

def on_message(client, userdata, msg):
    print(f"Message reçu sur {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.199", 1883, 60)
client.loop_forever()


import time
import random  # Remplace par tes vraies lectures

def publish_data():
    power = random.uniform(100, 500)  # Exemple
    temperature = random.uniform(20, 30)  # Exemple
    client.publish("smartplug/power", f'{{"power": {power:.2f}}}', qos=0)
    client.publish("smartplug/temperature", f'{{"temperature": {temperature:.2f}}}', qos=0)

while True:
    publish_data()
    time.sleep(1)
