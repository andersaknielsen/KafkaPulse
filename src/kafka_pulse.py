import asyncio
import struct
# using epoch as time
from time import time

from bleak import BleakClient

import src.plot_pulse as plot_pulse

from typing import Tuple

# Constants
HEART_RATE_MEASUREMENT = "00002A37-0000-1000-8000-00805F9B34FB"
DEVICE_ADDRESS = "E0:48:24:71:8C:B2"

def parse_heart_rate(data) -> Tuple:
    """Parses the heart rate measurement data"""
    flags = data[0]
    hr_fmt = flags & 0b00000001  # Heart Rate Value Format bit (0 = 8-bit, 1 = 16-bit)
    # snsr_cntct_spprtd = (flags & 0b00000100) >> 2  # Sensor contact supported bit
    # snsr_detect = (flags & 0b00001000) >> 3  # Sensor contact detected bit
    # nrg_expnd = (flags & 0b00010000) >> 4  # Energy expended status bit
    # rr_int = (flags & 0b00100000) >> 5  # RR-Interval bit

    if hr_fmt:
        hr_val, = struct.unpack_from("<H", data, 1)
    else:
        hr_val, = struct.unpack_from("<B", data, 1)
    
    # Print the HR value and the time
    print(f"HR Value: {hr_val} at {time()}")
    return (hr_val, time())


async def connect_and_receive_hr(address) -> None:
    """
    Connects to a BLE device at the given address and starts receiving heart rate notifications.
    Args:
        address (str): The MAC address of the BLE device to connect to.
    This function establishes a connection to the BLE device using the BleakClient.
    Once connected, it starts receiving heart rate measurements and processes them
    using the hr_val_handler function. The connection is maintained until the client
    is disconnected.
    """
    
    gather_data = []

    async with BleakClient(address) as client:
        connected = client.is_connected
        print(f"Connected: {connected}")

        def hr_val_handler(sender, data):
            """Notification handler for Heart Rate Measurement."""
            heart_rate_data = parse_heart_rate(data)
            gather_data.append(heart_rate_data)

        await client.start_notify(HEART_RATE_MEASUREMENT, hr_val_handler)

        while client.is_connected:
            await asyncio.sleep(1)
    
    # Plot the data
    plot_pulse.plot_data(pulse_data=gather_data)

def main() -> None:
    asyncio.run(connect_and_receive_hr(DEVICE_ADDRESS))

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
