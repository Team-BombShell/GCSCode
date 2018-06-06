from serial.serialutil import SerialException
import serial
import threading



class Comms:
    def __init__(self,ser_path,data,baud_rate=9600):
        
        try:
            connected=False
            self.temp_data_array = ''
            self.data = data
            self.ser = serial.Serial(
                port=ser_path,\
                baudrate=baud_rate,\
                parity=serial.PARITY_NONE,\
                stopbits=serial.STOPBITS_ONE,\
                bytesize=serial.EIGHTBITS,\
                timeout=0)
            def receive_data(data):
                if(len(data) >0):
                    if(not data == '~'):
                        self.temp_data_array += data
                    else:
                        self.temp_data_array = self.temp_data_array.split(',')
                        for i in range(len(self.temp_data_array)):
                            self.data[i].append(self.temp_data_array[i])
                            self.temp_data_array = ''
                       #print(self.data)

            def read_from_port(serial,connected):
                while not connected:
                    connected = True

                    while True:
                        
                        reading = serial.read().decode()
                        receive_data(reading)
            thread = threading.Thread(target=read_from_port,args=(self.ser,connected))
            thread.start()
        except SerialException:
            warnings.warn("COM port cannot be found. No data will be read. Try "
                          +"reconnecting the xbee then entering the port.")
            #TODO: Add a GUI feature that allows you to quickly change the port
 

            

    def tx(self,data):
        self.ser.write(data.encode())
    def halt(self):
        self.ser.close()
