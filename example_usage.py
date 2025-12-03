"""
Example usage of the MyStromSwitch class.
"""

import time
import logging
from mystrom_switch import MyStromSwitch, MyStromAPIError

# Configure logging to see info messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

IP_ADDRESS = "192.168.0.152"

def main():
    """Main function demonstrating MyStromSwitch usage."""
    try:
        # Initialize the switch
        switch = MyStromSwitch(IP_ADDRESS)
        
        # Example: Monitor the switch periodically
        print("\nMonitoring switch (press Ctrl+C to stop)...")
        while True:
            try:
                # Update all parameters
                switch.update_all()
                
                # Display current state
                print(f"\nCurrent Status:")
                print(f"  Temperature: {switch.temperature}°C")
                print(f"  Relay State: {'ON' if switch.relay_state else 'OFF'}")
                print(f"  Power: {switch.power}W")
                
                # Optional: Toggle the switch every 30 seconds
                # switch.toggle()
                
                time.sleep(10)
                
            except MyStromAPIError as e:
                print(f"Error updating switch: {e}")
                time.sleep(5)  # Wait before retrying
                
    except MyStromAPIError as e:
        print(f"Failed to initialize switch: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user")


def example_control():
    """Example demonstrating control functions."""
    try:
        switch = MyStromSwitch(IP_ADDRESS)
        
        # Turn on
        print("Turning on...")
        switch.turn_on()
        time.sleep(2)
        
        # Turn off
        print("Turning off...")
        switch.turn_off()
        time.sleep(2)
        
        # Toggle
        print("Toggling...")
        switch.toggle()
        
    except MyStromAPIError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
    # Or run: example_control()
