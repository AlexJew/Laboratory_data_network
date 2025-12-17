import requests
import time


myPlug = "192.168.0.152"


def read_status():
   url = "http://"+myPlug+"/report"
   response = requests.get(url)
   status = response.json()
   return status


def read_temperature():
   url = "http://"+myPlug+"/temp"
   response = requests.get(url)
   temperature = response.json()
   return temperature


def set_switch(state= None):
   if state not in [0, 1, None]:
       print("Invalid state. Use '0' or '1' (or leave empty to toggle)")
       return
   if state is None:
       url = f"http://{myPlug}/toggle"
   if state in [0, 1]:
       url = f"http://{myPlug}/relay?state={state}"
   response = requests.get(url)
   return


# Example usage
while True:
   status = read_status()
   print(status)


   temperature = read_temperature()
   print(temperature)


   set_switch()


   time.sleep(10)
