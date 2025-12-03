"""
MyStrom Switch API Client

This module provides a client for interacting with MyStrom Switch devices
over HTTP API.
"""

import requests
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyStromAPIError(Exception):
    """Custom exception for MyStrom API errors."""
    pass


class MyStromSwitch:
    """
    A client for interacting with MyStrom Switch devices.
    
    This class provides methods to control and monitor a MyStrom smart plug,
    including reading temperature, power consumption, relay state, and 
    controlling the switch.
    
    Attributes:
        ip_address (str): The IP address of the MyStrom Switch.
        timeout (int): Request timeout in seconds.
    """
    
    # API endpoints
    ENDPOINT_REPORT = "/report"
    ENDPOINT_TEMP = "/temp"
    ENDPOINT_TOGGLE = "/toggle"
    ENDPOINT_RELAY = "/relay"
    
    def __init__(self, ip_address: str, timeout: int = 5):
        """
        Initialize a new MyStromSwitch instance.
        
        Args:
            ip_address (str): The IP address of the MyStrom Switch device.
            timeout (int): Request timeout in seconds. Defaults to 5.
        
        Raises:
            MyStromAPIError: If unable to connect to the device.
        """
        self.ip_address = ip_address
        self.timeout = timeout
        self._base_url = f"http://{ip_address}"
        
        # Private attributes to store device state
        self._temperature: Optional[float] = None
        self._relay_state: Optional[bool] = None
        self._power: Optional[float] = None
        
        logger.info(f"Initializing MyStrom Switch at {ip_address}")
        self._validate_connection()
    
    @property
    def temperature(self) -> Optional[float]:
        """Get the current temperature reading."""
        return self._temperature
    
    @property
    def relay_state(self) -> Optional[bool]:
        """Get the current relay state."""
        return self._relay_state
    
    @property
    def power(self) -> Optional[float]:
        """Get the current power consumption in watts."""
        return self._power
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make an HTTP GET request to the device.
        
        Args:
            endpoint (str): API endpoint path.
            params (dict, optional): Query parameters.
        
        Returns:
            dict: JSON response from the device.
        
        Raises:
            MyStromAPIError: If the request fails.
        """
        url = f"{self._base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise MyStromAPIError(f"Request timeout connecting to {self.ip_address}")
        except requests.exceptions.ConnectionError:
            raise MyStromAPIError(f"Unable to connect to {self.ip_address}")
        except requests.exceptions.RequestException as e:
            raise MyStromAPIError(f"Request failed: {str(e)}")
    
    def _validate_connection(self) -> None:
        """
        Validate connection to the device.
        
        Raises:
            MyStromAPIError: If unable to connect to the device.
        """
        try:
            self.update_status()
            logger.info(f"Successfully connected to MyStrom Switch at {self.ip_address}")
        except MyStromAPIError as e:
            logger.error(f"Failed to connect to device: {str(e)}")
            raise
    
    def update_status(self) -> Dict[str, Any]:
        """
        Retrieve and update the current relay state and power consumption.
        
        Returns:
            dict: Status information including relay state and power.
        
        Raises:
            MyStromAPIError: If the request fails.
        """
        try:
            status = self._make_request(self.ENDPOINT_REPORT)
            self._relay_state = status.get("relay", False)
            self._power = status.get("power", 0.0)
            logger.debug(f"Status updated - Relay: {self._relay_state}, Power: {self._power}W")
            return status
        except MyStromAPIError as e:
            logger.error(f"Failed to update status: {str(e)}")
            raise
    
    def update_temperature(self) -> float:
        """
        Retrieve and update the current temperature from the device.
        
        Returns:
            float: The current temperature reading.
        
        Raises:
            MyStromAPIError: If the request fails.
        """
        try:
            temperature = self._make_request(self.ENDPOINT_TEMP)
            # Handle different response formats
            if isinstance(temperature, dict):
                self._temperature = temperature.get("temperature", temperature.get("compensated", 0.0))
            else:
                self._temperature = float(temperature)
            logger.debug(f"Temperature updated: {self._temperature}°C")
            return self._temperature
        except MyStromAPIError as e:
            logger.error(f"Failed to update temperature: {str(e)}")
            raise
    
    def update_all(self) -> None:
        """
        Update all device parameters (temperature, relay state, and power).
        
        Raises:
            MyStromAPIError: If any request fails.
        """
        self.update_temperature()
        self.update_status()
        logger.info(f"All parameters updated - Temp: {self._temperature}°C, "
                   f"Relay: {self._relay_state}, Power: {self._power}W")
    
    def toggle(self) -> bool:
        """
        Toggle the relay state (on to off or off to on).
        
        Returns:
            bool: The new relay state after toggling.
        
        Raises:
            MyStromAPIError: If the request fails.
        """
        try:
            response = self._make_request(self.ENDPOINT_TOGGLE)
            # Response format may vary, handle both dict and direct value
            if isinstance(response, dict):
                self._relay_state = response.get("relay", response.get("state", False))
            else:
                self._relay_state = bool(response)
            logger.info(f"Relay toggled to: {'ON' if self._relay_state else 'OFF'}")
            return self._relay_state
        except MyStromAPIError as e:
            logger.error(f"Failed to toggle relay: {str(e)}")
            raise
    
    def set_relay(self, state: bool) -> bool:
        """
        Set the relay to a specific state.
        
        Args:
            state (bool): Desired relay state. True for on, False for off.
        
        Returns:
            bool: The new relay state.
        
        Raises:
            MyStromAPIError: If the request fails.
            ValueError: If state is not a boolean.
        """
        if not isinstance(state, bool):
            raise ValueError("State must be a boolean (True/False)")
        
        try:
            state_value = 1 if state else 0
            response = self._make_request(self.ENDPOINT_RELAY, params={"state": state_value})
            # Response format may vary, handle both dict and direct value
            if isinstance(response, dict):
                self._relay_state = response.get("relay", response.get("state", False))
            else:
                self._relay_state = bool(response)
            logger.info(f"Relay set to: {'ON' if self._relay_state else 'OFF'}")
            return self._relay_state
        except MyStromAPIError as e:
            logger.error(f"Failed to set relay state: {str(e)}")
            raise
    
    def turn_on(self) -> bool:
        """
        Turn the relay on.
        
        Returns:
            bool: The new relay state (should be True).
        """
        return self.set_relay(True)
    
    def turn_off(self) -> bool:
        """
        Turn the relay off.
        
        Returns:
            bool: The new relay state (should be False).
        """
        return self.set_relay(False)
    
    def __repr__(self) -> str:
        """String representation of the MyStromSwitch instance."""
        return (f"MyStromSwitch(ip={self.ip_address}, "
                f"relay={'ON' if self._relay_state else 'OFF'}, "
                f"power={self._power}W, temp={self._temperature}°C)")
