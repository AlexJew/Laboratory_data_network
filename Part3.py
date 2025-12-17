import paho.mqtt.client as mqtt
import requests
import time
from MyStromSwitch import MyStromSwitch

# Adresse IP de la prise
ip_address_plug = "192.168.0.152"
ip_address_client = "192.168.0.199"

# --- Callbacks MQTT ---
class MyClient:

    def __init__(self, ip_address, plug):
        self.ip_address = ip_address
        self.plug = plug
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.message_callback_add("smartplug/relay/set", self.on_relay_set)
        self.client.connect(ip_address, 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc, properties):
        print("Connecté avec le code de retour :", rc)
        client.subscribe("smartplug/relay/set")

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
    myClient = MyClient(ip_address_client, myPlug)

    while True:
        try:
            status = myPlug.read_status()
            temperature = myPlug.read_temperature()

            # Get values
            power = status.get("power", 0)
            relay_state = status.get("relay", 0)   # 0 = fermé, 1 = ouvert
            temp = temperature.get("compensated", 0)

            # Conversion en texte pour MQTT
            relay_text = "open" if relay_state == 1 else "close"

            # Publication MQTT
            myClient.client.publish("smartplug/power", f'{{"power": {power}}}', qos=0)
            myClient.client.publish("smartplug/temperature", f'{{"temperature": {temp}}}', qos=0)
            myClient.client.publish("smartplug/relay/status", f'{{"relay": "{relay_text}"}}', qos=0)

            print(f"Publié: power={power} W, temp={temp} °C, relay={relay_text}")

        except Exception as e:
            print("Erreur de lecture ou publication:", e)

        time.sleep(1)
 