import requests
import time

class MyStromSwitch:

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.status = None
        self.temperature = None
        self.state = None

    def read_status(self):
        url = "http://"+self.ip_address+"/report"
        response = requests.get(url)
        self.status = response.json()
        return self.status

    def read_temperature(self):
        url = "http://"+self.ip_address+"/temp"
        response = requests.get(url)
        self.temperature = response.json()
        return self.temperature


    def set_switch(self, state= None):
        if state not in [0, 1, None]:
            print("Invalid state. Use '0' or '1' (or leave empty to toggle)")
            return
        if state is None:
            url = f"http://{self.ip_address}/toggle"
        if state in [0, 1]:
            url = f"http://{self.ip_address}/relay?state={state}"
            self.state = state
        response = requests.get(url)
        return

# Example usage
if __name__ == "__main__": 

    myPlug = MyStromSwitch("192.168.0.152")

    while True:
    
        print(myPlug.read_status())

        print(myPlug.read_temperature())

        myPlug.set_switch()

        time.sleep(10)
