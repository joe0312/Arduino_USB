#!/usr/bin/env python

import sys
import glob
import serial

##### Detected com port #####
if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')

else:
        raise EnvironmentError('Unsupported platform')

result = []

for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
print(result[0])


##### Transfer connecr message #####
if sys.argv[1] == "auto":
	ser=serial.Serial(result[0],115200)
	print("Connecting to USB ??")
	print "Input(Y or N) : ",sys.argv[2]
	ser.write(sys.argv[2].encode())

else:
	ser=serial.Serial(sys.argv[1],115200)
        print("Connecting to USB ??")
        print "Input(Y or N) : ",sys.argv[2]
        ser.write(sys.argv[2].encode())

print(ser)
