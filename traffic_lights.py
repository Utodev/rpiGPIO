"""
This simple python program controls two traffic lights (for a crossroad). It's designed to work with
the Raspberry Pi GPIO ports and so it requires the RpI.GPIO library, and of course a Raspeberry Pi.

You should be able to find the schematics for the trafic lights board together with this source code.
"""

import RPi.GPIO as GPIO
import time


# Define GPIO ports for each semaphore
S1_RED = 24
S1_YELLOW =  23
S1_GREEN =  18

S2_RED = 25
S2_YELLOW = 21 
S2_GREEN = 17

SEMAPHORE_GPIO = [[S1_RED,S1_YELLOW,S1_GREEN],[S2_RED,S2_YELLOW,S2_GREEN]];

#Define light statuses
LIGHT_RED = 0
LIGHT_YELLOW = 1
LIGHT_GREEN = 2

LIGHT_STATUSES = [LIGHT_RED,LIGHT_YELLOW,LIGHT_GREEN]

#Define the time in seconds that each traffic light status lasts
LIGHT_TIMES = [15,3,12] #Notice that time for red light = time for green + time for yellow

# Initial status for each semaphore
status = [LIGHT_RED, LIGHT_GREEN]
timeleft = [LIGHT_TIMES[LIGHT_RED],LIGHT_TIMES[LIGHT_GREEN]]


def setStatus(tlight):
	port_list = SEMAPHORE_GPIO[tlight]
	count = 0
	for port in port_list:
		GPIO.output(port, count == status[tlight]);
		count += 1;

def next(tlight):
	status[tlight]-=1
	if (status[tlight]<0):
		status[tlight] = 2
	timeleft[tlight] = LIGHT_TIMES[status[tlight]]
	setStatus(tlight)


# MAIN PROGRAM

#Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
for port_list in SEMAPHORE_GPIO:
    for port in port_list:
        GPIO.setup(port, GPIO.OUT)

# Test phase , turn all lights on, then off
for port_list in SEMAPHORE_GPIO:
    for port in port_list:
        GPIO.output(port,True)

time.sleep(1);

for port_list in SEMAPHORE_GPIO:
    for port in port_list:
        GPIO.output(port,False)

#Initialize
setStatus(0)
setStatus(1)

while True:
	print chr(27) + "[2J"
	for tlight in range (0,2):
		timeleft [tlight] -= 1;
		print "Traffic light" , tlight, "-->", timeleft[tlight], "seconds left"
		if (timeleft[tlight]==0): 
			next(tlight)
	time.sleep(1);

