#Prac 4 python file
#Commit 1

#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from threading import Timer

#setup GPIO pin selection method
GPIO.setmode(GPIO.BOARD)

#setup pins numbers for the different switches and outputs
reset = 31
frequency_pin = 33
stop = 35
display = 37

#setup variables for the program operation
isPrinting = 0                  #is the progam printing values, initialized to false as we will start printing in the main loop
frequency = 5                   #frequnecy of printing
data={1,2,3}                    #dummy data varible (will need to implement a 2D array or something similar)
global t

#setup GPIO input pins
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(frequency_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(display, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#function declarations
def reset_callback(pin):
	print("Reset Callback")

def frequency_pin_callback(pin):
	print("Frequency Callback")

def stop_callback(pin):
	print("Stop Callback")

def display_callback(pin):
        print("Display Callback")

def printing():
        global data
        for x in data:
                print(x, "<-") #, ", ") #, end="")
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
			print("Printing started")
			printing()
			isPrinting =1

		#Placeholder for later implementation
                print("Do something here in loop?")
                time.sleep(5)
except KeyboardInterrupt:
        GPIO.cleanup()  #cleanup GPIO on keyboard exit
	t.cancel()

GPIO.cleanup()  #cleanup GPIO on normal exit

