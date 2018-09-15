#Prac 4 python file
#Commit 1

#!/usr/bin/python3

import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os
from threading import Timer
from datetime import datetime

#Disable GPIO ste warnings
GPIO.setwarnings(False)

#setup GPIO pin selection method
GPIO.setmode(GPIO.BCM)

#setup pins numbers for the different switches and outputs
reset = 6
frequency_pin = 13
stop = 19
display = 26

#setup pin numbers for SPI interface
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

#setup variables for the program operation

isPrinting = 0                  	#is the progam printing values, initialized to false as we will start printing in the main loop
frequency = 3                   	#frequnecy of printing
data=[[0]*5 for i in range(5)]          #5 by 5 2D data variable
values = [0]*8			# array for storing ADC values from MCP3008
global t


#setup GPIO input pins
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(frequency_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(display, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#setup GPIO io pins for SPI interface
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#setup MCP3008
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)


#function declarations
def reset_callback(pin):
	print("Reset Callback")

def frequency_pin_callback(pin):
	print("Frequency Callback")

def stop_callback(pin):
	print("Stop Callback")

def display_callback(pin):
        print("Display Callback")
#Will become display function
#        for x in data:
#                print('{:8d} {:8d} {:2.1f}V {:2d} {:2d}%'.format(x[0],x[1],x[2],x[3],x[4]))

def printing():
        global data
        x = data[0]
        #use once have a function to get data
	#print('{:8d} {:8d} {:2.1f}V {:2d} {:2d}%'.format(x[0],x[1],x[2],x[3],x[4]))

	#using this print to get formatting correct
	print('{:%H:%M:%S} {:8d} {:2.1f}V {:2d} {:2d}%'.format(datetime.now().time(),x[1],x[2],x[3],x[4]))
        global t
	t = Timer(frequency,printing)
	t.start()

#setup edge detection
GPIO.add_event_detect(reset, GPIO.FALLING, bouncetime=200, callback=reset_callback)
GPIO.add_event_detect(frequency_pin, GPIO.FALLING, bouncetime=200, callback=frequency_pin_callback)
GPIO.add_event_detect(stop, GPIO.FALLING, bouncetime=200, callback=stop_callback)
GPIO.add_event_detect(display, GPIO.FALLING, bouncetime=200, callback=display_callback)

#setup GPIO output - might not need

#put into program loop
print("Setup done. Entering loop")
try:
        while True:
                if isPrinting != 1:	#if not printing then start printing
			print("Time   Timer  Pot  Temp  Light")
			printing()
			isPrinting =1

		#Placeholder for later implementation
                #print("Do something here in loop?")
                time.sleep(5)
except KeyboardInterrupt:
        GPIO.cleanup()  #cleanup GPIO on keyboard exit
	t.cancel()

GPIO.cleanup()  #cleanup GPIO on normal exit

