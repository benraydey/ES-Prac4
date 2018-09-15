#Prac 4 python file
#Commit 1

#!/usr/bin/python3

import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os
from threading import Timer
from datetime import datetime
from datetime import timedelta

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
isInitialPrint = 1			#(boolean) Is the program starting printing for the first time
isPrinting = 1                  	#(boolean) Is the program printing values
frequency = 3                   	#frequnecy of printing
data=[[0]*5 for i in range(5)]          #5 by 5 2D data variable
haveStartTime = 0			#(boolean) has startTime been obtained
rec_num = 0          		        #record number, ranges from 0 to 4. Initialized to 0. Increments after each adc reading

#global variables
global t				#timer variable
global startTime			#time of the first reading

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
	#get global variables
	global frequency
	global data
	global haveStartTime
	global t
	global rec_num

	#reset variables
	t.cancel()				#stop timer
	frequency = 0.5
	data=[[0]*5 for i in range(5)]          #5 by 5 2D data variable
	haveStartTime = 0
	rec_num = 0

	#clear the console and restart printing
	print(chr(27)+"[2J")
	print("Reset Callback")
	print('{:8s} {:8s} {:4s} {:s} {:s}'.format("Time","Timer","Pot","Temp","Light"))
	read_data()

def frequency_pin_callback(pin):
	#this function will only change the frequency after the next value is recorded/printed
	print("Frequency Callback")
	global frequency
	if frequency == 0.5:
		frequency = 1
	elif frequency == 1:
		frequency = 2
	else:
		frequency = 0.5


def stop_callback(pin):
	print("Stop Callback")
	global t
	global isPrinting

	if isPrinting == 1:
		t.cancel()
		isPrinting = 0
	elif isPrinting == 0:
		isPrinting = 1
		read_data()

def display_callback(pin):
        print("Display Callback")
	global data
	for i in range(rec_num,len(data)):
		x = data[i]
		print('{:%H:%M:%S} 0{:7s} {:3.1f}V {:<3d}C {:2d}%'.format(x[0].time(),x[1],x[2],x[3],x[4]))
	for i in range(rec_num):
		x = data[i]
		print('{:%H:%M:%S} 0{:7s} {:3.1f}V {:<3d}C {:2d}%'.format(x[0].time(),x[1],x[2],x[3],x[4]))

	#legacy
	#was using this code to get everything working, can comment out once data has correct values
	#	time = datetime.now()
	#	timerValue = str(time - startTime)[:7]
	#	print('{:%H:%M:%S} 0{:7s} {:3.1f}V {:<3d}C {:2d}%'.format(time.time(),timerValue,x[2],x[3],x[4]))


def printing():
	#legacy
	#set the time of first reading
	#global startTime
	#global haveStartTime
	#if haveStartTime != 1:
	#	startTime = datetime.now()
	#	haveStartTime = 1

	#print the required data
	global data
	if rec_num == 0:
        	x = data[4]
	else:
		x = data[rec_num-1]
        #should be working, can uncommment once the right values are stored in data
	print('{:%H:%M:%S} 0{:7s} {:3.1f}V {:<3d}C {:2d}%'.format(x[0].time(),x[1],x[2],x[3],x[4]))

	#legacy
	#was using this code to get formatting correct, can comment out once data has correct values
	#time = datetime.now()
	#timerValue = str(time - startTime)[:7]
	#print('{:%H:%M:%S} 0{:7s} {:3.1f}V {:<3f}C {:2f}%'.format(time.time(),timerValue,x[2],x[3],x[4]))

	#start the timer again for periodic functioning
	global t
	t = Timer(frequency,read_data)
	t.start()

def read_data():
    global rec_num
    global data
    global startTime
    global haveStartTime

    #find time
    time = datetime.now()

    #set the time of first reading
    if haveStartTime != 1:
	startTime = time
	haveStartTime = 1

    #store time and timerValue
    data[rec_num][0] = time
    data[rec_num][1] = str(time - startTime)[:7]

    #read in adc values and convert to appropriate units
    data[rec_num][2] = conv_10bit_to_3V3(mcp.read_adc(0))
    data[rec_num][3] = conv_10bit_to_deg_celsius(mcp.read_adc(1))
    data[rec_num][4] = conv_10bit_to_perc(mcp.read_adc(2))

    rec_num += 1
    if rec_num == 5:
        rec_num = 0

    printing()


def conv_10bit_to_3V3(val):
#converts a 10 bit ADC value to a voltage in range 0 - 3.3V
    return round(val*3.3/1023,1)

def conv_10bit_to_deg_celsius(val):
#converts a 10 bit ADC value to a temperature in degrees Celsius

    return int(round(( (val*3.3/1023) - 0.5 ) / 0.01))    #Equation from MCP9700 datasheet

def conv_10bit_to_perc(val):
#converts a 10 bit ADC value to a percentage
    return int(round(val*100/1023))

#setup edge detection
GPIO.add_event_detect(reset, GPIO.FALLING, bouncetime=200, callback=reset_callback)
GPIO.add_event_detect(frequency_pin, GPIO.FALLING, bouncetime=200, callback=frequency_pin_callback)
GPIO.add_event_detect(stop, GPIO.FALLING, bouncetime=200, callback=stop_callback)
GPIO.add_event_detect(display, GPIO.FALLING, bouncetime=200, callback=display_callback)

#setup GPIO output - might not need

#purely testing things here
#print(len(data))

#put into program loop
print("Setup done. Entering loop")
try:
        while True:

          if isInitialPrint == 1:	#start printing for the first time
            print('{:8s} {:8s} {:4s} {:s} {:s}'.format("Time","Timer","Pot","Temp","Light"))
            read_data()    		#Read data from ADC
            isInitialPrint = 0

	  #Placeholder for later implementation
          #print("Do something here in loop?")
          time.sleep(5)
          #time.sleep(0.5)
except KeyboardInterrupt:
        GPIO.cleanup()  #cleanup GPIO on keyboard exit
        t.cancel()

GPIO.cleanup()  #cleanup GPIO on normal exit

