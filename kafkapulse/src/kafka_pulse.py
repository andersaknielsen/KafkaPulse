import asyncio
import struct
from typing import Tuple, List
from time import time
import random

from bleak import BleakClient

import plot_pulse as plot_pulse

# Constants
HEART_RATE_MEASUREMENT = "00002A37-0000-1000-8000-00805F9B34FB"
DEVICE_ADDRESS = "E0:48:24:71:8C:B2"

class HeartRateDataCollector:
    def __init__(self):
        self.data: List[Tuple[int, float]] = []

    def add_data(self, heart_rate: int, timestamp: float) -> None:
        self.data.append((heart_rate, timestamp))

    def plot_data(self) -> None:
        plot_pulse.plot_data(pulse_data=self.data)

class HeartRateMonitor:
    def __init__(self, address: str, data_collector: HeartRateDataCollector):
        self.address = address
        self.data_collector = data_collector

    def parse_heart_rate(self, data) -> Tuple[int, float]:
        """Parses the heart rate measurement data"""
        flags = data[0]
        hr_fmt = flags & 0b00000001  # Heart Rate Value Format bit (0 = 8-bit, 1 = 16-bit)

        if hr_fmt:
            hr_val, = struct.unpack_from("<H", data, 1)
        else:
            hr_val, = struct.unpack_from("<B", data, 1)
        
        # Print the HR value and the time
        print(f"HR Value: {hr_val} at {time()}")
        return (hr_val, time())


    async def connect_and_receive_hr(self, plot_data = True) -> None:
        """
        Connects to a BLE device at the given address and starts receiving heart rate notifications.
        """
        async with BleakClient(self.address) as client:
            connected = client.is_connected
            print(f"Connected: {connected}")

            def heart_rate_notification_handler(sender, data):
                """Notification handler for Heart Rate Measurement."""
                heart_rate_data = self.parse_heart_rate(data)
                self.gather_data.append(heart_rate_data)

            await client.start_notify(HEART_RATE_MEASUREMENT, heart_rate_notification_handler)

            while client.is_connected:
                await asyncio.sleep(1)
        
        if plot_data:
            # Plot the data
            self.data_collector.plot_data()

    async def mock_heart_rate(self, plot_data = False) -> None:
        """
        Simulates heart rate data by generating a random heart rate value between 50 and 70 every second for 10 seconds.
        """
        for _ in range(10):
            heart_rate = random.randint(50, 70)
            timestamp = time()
            print(f"Mock HR Value: {heart_rate} at {timestamp}")
            self.data_collector.add_data(heart_rate, timestamp)
            await asyncio.sleep(0.1)
            
        if plot_data:
            self.data_collector.plot_data()


def main() -> None:
    data_collector = HeartRateDataCollector()
    monitor = HeartRateMonitor(DEVICE_ADDRESS, data_collector)
    # asyncio.run(monitor.connect_and_receive_hr(plot_data=True))
    # Use the mock heart rate method for testing
    asyncio.run(monitor.mock_heart_rate(plot_data=False))

if __name__ == "__main__":
    """This module connects to a BLE device and receives heart rate notifications.
    Functions:
        parse_heart_rate(data):
            Parses the heart rate measurement data without bitstruct.
                data (bytes): The raw data received from the BLE device.
            Returns:
                None
        run(address):
            Returns:
                None
    Constants:
        HEART_RATE_MEASUREMENT: (str): UUID for the Heart Rate Measurement characteristic.
        DEVICE_ADDRESS: (str): MAC address of the BLE device to connect to."""
    main()
