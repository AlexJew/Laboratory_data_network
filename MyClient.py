import paho.mqtt.client as mqtt
import requests
import time
from MyStromSwitch import MyStromSwitch

# Adresses IP
ip_address_plug = "192.168.0.152"
ip_address_broker = "192.168.0.199"

# Définition de la classe myClient
class MyClient:

    def __init__(self, ip_address_broker, plug):
        self.ip_address = ip_address_broker
        self.plug = plug
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.connect(ip_address_broker, 1883, 60)
        self.client.message_callback_add(f"plug/{self.plug.ip_address}/relay/set", self.on_relay_set)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc, properties):
        print("Connecté avec le code de retour :", rc)
        self.client.subscribe(f"plug/{self.plug.ip_address}/relay/set")
    
    def publish_temperature(self, temperature):
        self.client.publish(f"plug/{self.plug.ip_address}/temperature", f'{{{temperature}}}', qos=0)
    
    def publish_power(self, power):
        self.client.publish(f"plug/{self.plug.ip_address}/power", f'{{{power}}}', qos = 0)
    
    def publish_relay_status(self, relay_status):
        self.client.publish(f"plug/{self.plug.ip_address}/relay/status", f'{{{relay_status}}}', qos = 0)

    def on_relay_set(self, client, userdata, msg):
        command = msg.payload.decode()
        print(f"Commande reçue : {command}")
        if command == "open":
            self.plug.set_switch(1)   # 1 = relais ON
            print("Relais ouvert")
        elif command == "close":
            self.plug.set_switch(0)   # 0 = relais OFF
            print("Relais fermé")
    

# Example usage
if __name__ == "__main__": 

    # Définition du plug
    myPlug = MyStromSwitch(ip_address_plug)

    # Définition du client MQTT
    myClient = MyClient(ip_address_broker, myPlug)

    while True:
        try:

            # Lecture des valeurs de prise
            power = myPlug.read_power()
            temperature = myPlug.read_temperature()
            relay_status = myPlug.read_status()['relay']

            # Conversion du status en texte pour MQTT
            relay_text = "open" if relay_status == 1 else "close"

            # Publication des valeurs sur le broker
            myClient.publish_power(power)
            myClient.publish_temperature(temperature)
            myClient.publish_relay_status(relay_text)

        except Exception as e:
            print("Erreur de lecture ou publication:", e)

        time.sleep(1)
