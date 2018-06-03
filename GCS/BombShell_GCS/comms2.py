from serial.serialutil import SerialException
import serial

import warnings
from digi.xbee.devices import XBeeDevice

class Comms:
    def __init__(self,ser_path,baud_rate):
        self.device = XBeeDevice(ser_path,baud_rate)

        try:
            device.open()

            def data_received(xbee_message):
                
                received_addr = xbee_message.remote_device.get_64bit_addr()
                
                print(received_addr)

                data = xbee_message.data.decode()

                print(data)

            device.add_data_received_callback(data_recieved)

        finally:
            if device is not None and device.is_open():
                device.close()
                
        

        
