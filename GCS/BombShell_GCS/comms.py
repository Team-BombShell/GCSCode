from serial.serialutil import SerialException
import serial

import warnings
from digi.xbee.devices import XBeeDevice

class Comms:
    def __init__(self,ser_path,data,baud_rate=9600):
        device = XBeeDevice(ser_path,baud_rate)
        
        
        try:
            device.open()

            def data_received(xbee_message):

                received_addr = xbee_message.remote_device.get_64bit_addr()
                    
                data_in = xbee_message.data.decode()
             
                for i in range(len(data_in)):
                    data[i].append(data_in[i])
               
            device.add_data_received_callback(data_received)
            
        except SerialException:
            warnings.warn("COM port cannot be found. No data will be read. Try "
                          +"reconnecting the xbee then entering the port.")
            #TODO: Add a GUI feature that allows you to quickly change the port

            
        finally:
            if device is not None and device.is_open():
                device.close()
                
        

        
