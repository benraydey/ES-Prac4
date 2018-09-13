#Prac 4 python file
#Commit 1

#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from threading import Timer

#setup GPIO pin selection method
GPIO.setmode(GPIO.BOARD)

#setup pins numbers for the different switches and outputs
reset = 3
frequency_pin = 5
stop = 7
display = 11

#setup variables for the program operation
isDisplaying = 1                #is the progam displaying values, initialized to true
frequency = 0.5                 #frequnecy of printing
data[]={1,2,3}                  #dummy data varible (will need to implement a 2D array or something similar)

#setup GPIO input pins
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(frequency_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dsiplay, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#function declarations
def reset_callback(pin):
	print("reset Callback")

def frequency_pin_callback(pin):
	print("Frequency Callback")

def stop_callback(pin):
	print("Stop Callback")

def stop_callback(pin):
        print("Display Callback")

def printing():
        global data
        for x in data:
                print(x)
        Timer(freqency,printing).start()

#setup edge detection
GPIO.add_event_detect(reset, GPIO.FALLING, bouncetime=200, callback=reset_callback)
GPIO.add_event_detect(frequency_pin, GPIO.FALLING, bouncetime=200, callback=frequency_pin_callback)
GPIO.add_event_detect(stop, GPIO.FALLING, bouncetime=200, callback=stop_callback)
GPIO.add_event_detect(display, GPIO.FALLING, bouncetime=200, callback=display_callback)

#setup GPIO output

#start printing
t = Timer(freqency,printing).start()

#put into program loop
print("Setup done. Entering loop")
try
        while True:
                #Placeholder for later implementation
                print("Data")
                time.sleep(5)
except KeyboardInterrupt:
        GPIO.cleanup()  #cleanup GPIO on keyboard exit

GPIO.cleanup()  #cleanup GPIO on normal exit

