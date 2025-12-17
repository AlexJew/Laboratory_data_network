import paho.mqtt.client as mqtt
import requests
import time

# Adresse IP de la prise
myPlug = "192.168.0.152"


#--- Fonctions pour interagir avec la prise MyStrom ---
def read_status():
    url = "http://" + myPlug + "/report"
    response = requests.get(url)
    return response.json()   # Puissance

def read_temperature():
    url = "http://" + myPlug + "/temp"
    response = requests.get(url)
    return response.json()   # Température

def set_switch(state=None):
    if state not in [0, 1, None]:
        print("Invalid state. Use '0' or '1' (or leave empty to toggle)")
        return
    if state is None:
        url = f"http://{myPlug}/toggle"
    else:
        url = f"http://{myPlug}/relay?state={state}"
    response = requests.get(url)
    return response.json()

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
while True:
    try:
        status = read_status()
        temperature = read_temperature()

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

client.loop_forever()
 