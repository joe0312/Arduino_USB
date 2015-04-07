#!/usr/bin/env python

import sys
import serial
import serial.tools.list_ports


###### Usage here documents ######
heredoc="""

NAME
	ui_python - Connect to controller and control USB connection

SYNOPSIS
	ui_python deviceopt [switchopt]

DESCRIPTION
	deviceopt
		Connect to controller(Arduino) with device com port(deviceopt)
		If you don't know the corresponding com port,you can use "auto" to detect the device and list it

	switchopt
		Use switch signal(switchopt) to control USB connection
		"Y"  : connect USB
		"N"  : disconnect USB

EXAMPLE
	ui_python auto
		Detected device com port and try to communicate with Arduino
		When success will return corresponding com port

	ui_python /dev/ttyUSB0 Y
		Connect USB switch with "/dev/ttyUSB0" com port

"""


##### Detected com port #####
def detected_com_port(deviceopt):
	if deviceopt == "auto":
		devicelist = serial.tools.list_ports.comports()
	else:
		devicelist = [(deviceopt,deviceopt,"user")]
	for ports in devicelist:
		try:
			ser = serial.Serial(ports[0],115200,timeout=1)
			msg=ser.readline()
			ser.write('S')
			msg=ser.readline()
			if msg == "Connect received: S\r\n":
				deviceport=ports[0]
				break
		except (OSError, serial.SerialException):
			pass
	try:
		print("Device com port is %s"%(deviceport))
		return deviceport
	except (NameError):
		print("Error: No detected com port")
		sys.exit(1)


##### Receive message and analysis #####
if len(sys.argv) == 2 :
	deviceport=detected_com_port(sys.argv[1])
	sys.exit(1)
elif len(sys.argv) == 3 :
	deviceport=detected_com_port(sys.argv[1])
	switchopt=sys.argv[2]
else:
	print "Error: invalid parameter format"
	print(heredoc)
	sys.exit(1)


##### Transfer connect message #####
if switchopt in "YN":
	ser=serial.Serial(deviceport,115200,timeout=1)
	print("Connecting to USB ??")
	msg=ser.readline()
	ser.write(switchopt)
	print "Input(Y or N) : ",switchopt
else:
	print("Error: Switch options should be connect\"Y\" or dicconnect\"N\"")
	sys.exit(1)

