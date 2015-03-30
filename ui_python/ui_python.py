#!/usr/bin/env python

import sys
import serial
import serial.tools.list_ports

###### Usage here documents ######
message="""

NAME
	ui_python - Connect to controller and control USB connection

SYNOPSIS
	ui_python deviceopt actionopt

DESCRIPTION
	deviceopt
		Connect to controller(Arduino) with device com port(deviceopt)
		If you don't know the corresponding com port,you can use "auto" to detect the device

	actionopt
		Transfer action signal(actionopt) to controller(Arduino)
		"Y/y"  : connect USB
		"N/n"  : disconnect USB
		"scan" : detected the device com port and list it
"""


##### Receive message #####
if len(sys.argv) == 3 :
	deviceopt=sys.argv[1]
	actionopt=sys.argv[2]
else:
	print "Error: invalid parameter format"
	print(message)
	sys.exit(1)


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
		print("Device com port is %s"%(device))
	except (NameError):
		print("Error: No detected com port(Please plug in device)")
		sys.exit(1)
else:
	try:
		ser=serial.Serial(deviceopt,115200,timeout=1)
		msg=ser.readline()
		ser.write('C')
		msg=ser.readline()
		if msg != "Connect received: C\r\n":
			print("Error: \"%s\" can't connect to Arduino"%(deviceopt))
			sys.exit(1)
	except (OSError, serial.SerialException):
		print("Error: Invalid device \"%s\""%(deviceopt))
		sys.exit(1)


##### Transfer connect message #####
if actionopt == "scan":
	sys.exit(1)
elif actionopt in "YyNn":
	print("Connecting to USB ??")
	msg=ser.readline()
	ser.write(actionopt)
	print "Input(Y or N) : ",actionopt
else:
	print("Error: Action should be connect\"Y\" or dicconnect\"N\" or scan device\"scan\"")
	sys.exit(1)

