import paho.mqtt.client as mqtt
import requests
import time
from MyStromSwitch import MyStromSwitch

# Adresse IP de la prise
ip_address = "192.168.0.152"

# --- Callbacks MQTT ---
def on_connect(client, userdata, flags, rc):
    print("Connecté avec le code de retour :", rc)
    # Abonnement au topic du relais
    client.subscribe("smartplug/relay/set")

def on_relay_set(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Commande reçue : {command}")
    if command == "open":
        set_switch(1)   # 1 = relais ON
        print("Relais ouvert")
    elif command == "close":
        set_switch(0)   # 0 = relais OFF
        print("Relais fermé")

# --- Configuration du client MQTT ---
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.message_callback_add("smartplug/relay/set", on_relay_set)

client.connect("192.168.0.199", 1883, 60)

# --- Boucle principale ---
if __name__ == "__main__": 

    myPlug = MyStromSwitch(ip_address)

    while True:
        try:
            status = myPlug.read_status()
            temperature = myPlug.read_temperature()

            #
            power = status.get("power", 0)
            relay_state = status.get("relay", 0)   # 0 = fermé, 1 = ouvert
            temp = temperature.get("compensated", 0)

            # Conversion en texte pour MQTT
            relay_text = "open" if relay_state == 1 else "close"

            # Publication MQTT
            client.publish("smartplug/power", f'{{"power": {power}}}', qos=0)
            client.publish("smartplug/temperature", f'{{"temperature": {temp}}}', qos=0)
            client.publish("smartplug/relay/status", f'{{"relay": "{relay_text}"}}', qos=0)

            print(f"Publié: power={power} W, temp={temp} °C, relay={relay_text}")

        except Exception as e:
            print("Erreur de lecture ou publication:", e)

        time.sleep(1)
    
 