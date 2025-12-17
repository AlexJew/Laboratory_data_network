import paho.mqtt.client as mqtt
import requests
import time

# Adresses IP
ip_address_plug = "192.168.0.152"
ip_address_broker = "192.168.0.199"

# Définition de la classe myController
class MyController:

    def __init__(self, ip_address_broker, ip_address_plug):
        self.ip_address_broker = ip_address_broker
        self.ip_address_plug = ip_address_plug
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.connect(ip_address_broker, 1883, 60)
        self.client.message_callback_add(f"plug/{self.ip_address_plug}/relay/status", self.on_status)
        self.client.message_callback_add(f"plug/{self.ip_address_plug}/temperature", self.on_temperature)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc, properties):
        print("Connecté avec le code de retour :", rc)
        client.subscribe(f"plug/{self.ip_address_plug}/relay/set")
        client.subscribe(f"plug/{self.ip_address_plug}/relay/status")
        client.subscribe(f"plug/{self.ip_address_plug}/temperature")

    def on_status(self, client, userdata, msg):
        status = msg.payload.decode()
        print(f"Statut du relais: {status}")
    
    def on_temperature(self, client, userdata, msg):
        temperature = msg.payload.decode()
        print(f"Temperature: {temperature}")

    def set_switch(self, state=None):
        
        self.client.publish(f"plug/{self.plug.ip_address}/relay/set", f'{{"power": {power}}}', qos = 0)

# Example usage
if __name__ == "__main__": 

    # Définition du client MQTT
    myController = MyController(ip_address_broker, ip_address_plug)

    while True:

        time.sleep(1)