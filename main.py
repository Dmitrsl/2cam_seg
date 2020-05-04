import glob
import serial

ports = glob.glob('/dev/tty[A-Za-z]*')
print(ports)
 
result = []
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        result.append(port)
    except (OSError, serial.SerialException):
        pass
print(result)