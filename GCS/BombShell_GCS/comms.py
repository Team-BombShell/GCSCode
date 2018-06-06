from serial.serialutil import SerialException
import serial

import warnings
from digi.xbee.devices import XBeeDevice

class Comms:
    def __init__(self,ser_path,data,baud_rate=9600):
        self.device = XBeeDevice(ser_path,baud_rate)
        
       
        
        
        try:
            self.device.open()
            
            def data_received(xbee_message):

                received_addr = xbee_message.remote_device.get_64bit_addr()
                print(received_addr)   
                data_in = xbee_message.data.decode()
                print(data_in)
                for i in range(len(data_in)):
                    data[i].append(data_in[i])
               
            self.device.add_data_received_callback(data_received)
            print("hello")
        except SerialException:
            warnings.warn("COM port cannot be found. No data will be read. Try "
                          +"reconnecting the xbee then entering the port.")
            #TODO: Add a GUI feature that allows you to quickly change the port

            
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
         
                
    def tx(self,data):
        try:
            self.device.open()
            self.device.send_data_broadcast(data)
        except SerialException:
            pass
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()

        
