from serial.serialutil import SerialException
import serial
import threading
import warnings
import queue
import math


class Comms:
    def __init__(self,ser_path,data,raw_data,baud_rate=9600):
        
        try:
            self.rowan = queue.Queue()
            self.connected=False
            self.temp_data_array = ''
            self.data = data
            self.raw_data = raw_data
            self.raw_file = open('raw.dat','a',newline='')
            self.ser = serial.Serial(
                port=ser_path,\
                baudrate=baud_rate,\
                parity=serial.PARITY_NONE,\
                stopbits=serial.STOPBITS_ONE,\
                bytesize=serial.EIGHTBITS,\
                timeout=0)
            def receive_data(data):
                #print(self.temp_data_array)
                if(len(data) >0):
                    if(not data == '\n'):
                        self.temp_data_array += data
                    else:
                        self.temp_data_array = self.temp_data_array.split(',')
                        length = len(self.temp_data_array)
                        if(length == 16):
                            for i in range(length):
                                if (i == 14):
                                    pythag = math.sqrt(self.data[12]**2 + self.data[13]**2)
                                    self.data[i].append(pythag)
                                    print(pythag)
                                else:
                                    self.data[i].append(self.temp_data_array[i])
                        self.temp_data_array = ''
                        self.connected = False
                       # print(self.data)

            def read_from_port(serial,connected):
                while True:
                    #print('a')
                    if(not self.rowan.empty()):
                        serial.write(self.rowan.get())
                    reading = serial.read()
                    if(len(reading) > 0):
                        self.raw_file.write(reading.decode(encoding='mbcs'))
                        self.raw_file.flush()
                    
                    
                        reading = reading.decode(encoding='mbcs')
                    
                    
                        if self.temp_data_array == '' and reading == '$':
                            self.connected = True
                        

                        if self.connected:
                           # print(reading)
                            receive_data(reading)
                        
                              
                    
            
            self.thread = threading.Thread(target=read_from_port,args=(self.ser,self.connected))
            self.thread.start()
        except SerialException:
            warnings.warn("COM port cannot be found. No data will be read. Try "
                          +"reconnecting the xbee then entering the port.")
            #TODO: Add a GUI feature that allows you to quickly change the port
 

            

    def tx(self,data):
        self.rowan.put(data.encode())
    def halt(self):
        #self.thread.join()
        #self.ser.close()
        pass
