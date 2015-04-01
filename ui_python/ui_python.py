#!/usr/bin/env python

import sys
import serial
import serial.tools.list_ports


###### Usage here documents ######
heredoc="""

{BLUE}NAME{WHITE}
	ui_python - Connect to controller and control USB connection

{BLUE}SYNOPSIS{WHITE}
	ui_python {RED}deviceopt{WHITE}
	ui_python {RED}deviceopt switchopt{WHITE}

{BLUE}DESCRIPTION{WHITE}
	{RED}deviceopt{WHITE}
		Connect to controller(Arduino) with device com port(deviceopt)
		If you don't know the corresponding com port,you can use {RED}"auto"{WHITE} to detect the device and list it

	{RED}switchopt{WHITE}
		Use switch signal(switchopt) to control USB connection
		{RED}"Y"{WHITE}  : connect USB
		{RED}"N"{WHITE}  : disconnect USB
"""


##### Detected com port #####
def detected_com_port(deviceopt):
	if deviceopt == "auto":
		for ports in serial.tools.list_ports.comports():
			try:
				ser = serial.Serial(ports[0],115200,timeout=1)
				msg=ser.readline()
				ser.write('C')
				msg=ser.readline()
				if msg == "Connect received: C\r\n":
					devicescan=ports[0]
					break
			except (OSError, serial.SerialException):
				pass
		try:
			print("Device com port is %s"%(devicescan))
			deviceopt = devicescan
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
	return deviceopt

##### Receive message and analysis #####
if len(sys.argv) == 2 :
	deviceopt=detected_com_port(sys.argv[1])
	sys.exit(1)
elif len(sys.argv) == 3 :
	deviceopt=detected_com_port(sys.argv[1])
	switchopt=sys.argv[2]
else:
	print "Error: invalid parameter format"
	print(heredoc.format(RED="\33[31m",BLUE="\33[34m",WHITE="\33[37m"))
	sys.exit(1)


##### Transfer connect message #####
if switchopt in "YN":
	ser=serial.Serial(deviceopt,115200,timeout=1)
	print("Connecting to USB ??")
	msg=ser.readline()
	ser.write(switchopt)
	print "Input(Y or N) : ",switchopt
else:
	print("Error: Switch options should be connect\"Y\" or dicconnect\"N\"")
	sys.exit(1)

