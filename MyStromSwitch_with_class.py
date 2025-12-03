import requests
import time

IP_ADDRESS = "192.168.0.152"

class Plug():
    """
    A class to interact with a MyStrom Switch device.
    
    This class provides methods to control and monitor a MyStrom smart plug,
    including reading temperature, power consumption, relay state, and 
    toggling the switch on/off.
    
    Attributes:
        ip_address (str): The IP address of the MyStrom Switch.
        temperature (float): The current temperature reading from the device.
        state (bool): The current relay state (True for on, False for off).
        power (float): The current power consumption in watts.
    """
    
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.temperature = None
        self.state = None
        self.power = None
        print(f"New plug with IP {ip_address}\n")
        self.update()
    
    def update_status(self):
        url_status = f"http://{self.ip_address}/report"
        status = requests.get(url_status).json()
        self.state = status["relay"]
        self.power = status["power"]
        print(f"State: {self.state}")
        print(f"Power: {self.power}\n")
        return status
    
    def update_temperature(self):
        url_temperature = f"http://{self.ip_address}/temp"
        temperature = requests.get(url_temperature).json()
        self.temperature = temperature
        print(f"Temperature: {temperature}\n")
        return temperature
    
    def update(self):
        self.update_temperature()
        self.update_status()
    
    def toggle_switch(self):
        url_state = f"http://{self.ip_address}/toggle"
        state = requests.get(url_state).json()
        self.state = state
        print(f"State: {state}")
        return state
    
    def set_switch(self, state = None):
        if state not in [0, 1, None]:
            print("Invalid state. Use '0' or '1' (or leave empty to toggle)")
            return
        if state is None:
            return self.toggle_switch()
        if state in [0, 1]:
            url_state = f"http://{self.ip_address}/relay?state={state}"
            state = requests.get(url_state).json()
            self.state = state
            print(f"State: {state}\n")
            return state

# Example usage
# plug = Plug(IP_ADDRESS)

# while True:
#     plug.update_status()

#     plug.update_temperature()

#     plug.set_switch()

#     time.sleep(10)