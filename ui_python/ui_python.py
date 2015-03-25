#!/usr/bin/env python

import sys
import serial
import serial.tools.list_ports


##### Receive message #####
if len(sys.argv) != 3 :
	print "Input format error(python)!!"
	sys.exit(1)
elif sys.argv[2] != "Y" and sys.argv[2] != "N":
	print("Switch input error(python)!!") 
	sys.exit(1)
else:
	deviceopt=sys.argv[1]
	switchopt=sys.argv[2]


##### Detected com port #####
if deviceopt == "auto":
	ports=list(serial.tools.list_ports.comports())

	for i in range(0,len(ports)):
		try:
			ser = serial.Serial(ports[i][0],115200,timeout=1)
			msg=ser.readline()
			ser.write('C')
			msg=ser.readline()
			ser.close()
			if msg == "Connect received: C\r\n":
				device=ports[i][0]
				break
		except (OSError, serial.SerialException):
			pass
	print "Device com port is ",device
	ser=serial.Serial(device,115200)
else:
	try:
		ser=serial.Serial(deviceopt,115200)
	except (OSError, serial.SerialException):
		print("Device input error(python)!!")
		sys.exit(1)


##### Transfer connecr message #####
print("Connecting to USB ??")
print "Input(Y or N) : ",switchopt
ser.write(switchopt)

# print(ser)
