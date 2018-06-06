import serial

ser = serial.Serial(
    port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1
lines = ''

while True:
    line = ser.read()
    lines += line.decode()
    if(len(line) >0):
        print(lines)
ser.write("Hello")

ser.close()
