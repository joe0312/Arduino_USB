#!/usr/bin/env python

import sys
import serial
import serial.tools.list_ports


##### Receive message #####
if len(sys.argv) != 3 :
	print "Error: input error parameter"
	sys.exit(1)
else:
	deviceopt=sys.argv[1]
	switchopt=sys.argv[2]


##### Detected com port #####
if deviceopt == "auto":
	for ports in serial.tools.list_ports.comports():
		try:
			ser = serial.Serial(ports[0],115200,timeout=1)
			msg=ser.readline()
			ser.write('C')
			msg=ser.readline()
			if msg == "Connect received: C\r\n":
				device=ports[0]
				break
		except (OSError, serial.SerialException):
			pass
	try:
		print "Device com port is ",device
	except (NameError):
		print("not detection(Please plug in device)")
		sys.exit(1)
else:
	try:
		ser=serial.Serial(deviceopt,115200,timeout=1)
		msg=ser.readline()
		ser.write('C')
		msg=ser.readline()
		if msg != "Connect received: C\r\n":
			print("Error: invalid device \"%s\""%(deviceopt))
			sys.exit(1)
	except (OSError, serial.SerialException):
		print("Error: invalid device \"%s\""%(deviceopt))
		sys.exit(1)



##### Transfer connect message #####
if switchopt == "D":
	sys.exit(1)
elif switchopt in "YyNn":
	print("Connecting to USB ??")
	print "Input(Y or N) : ",switchopt
	msg=ser.readline()
	ser.write(switchopt)
else:
	print("Error: action should be connect\"Y\" or dicconnect\"N\"")
	sys.exit(1)

# print(ser)
