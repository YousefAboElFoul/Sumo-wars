#The code contains all the basic moving of the car such as:
#Forward, Backward, Rotate left and right
#This basic code will be combined with sensors to build the complete algorithm
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD) #Consider the label of GPIO, not the pin number

m1pin1=3
m1pin2=5

m2pin1=11
m2pin2=7

#Motor 1 setup m1P -> 2, m1N -> 3, m1E -> 4
GPIO.setup(m1pin1,GPIO.OUT) #Input 1
GPIO.setup(m1pin2,GPIO.OUT) #Input 2

#PWM setup for motor 1, 50 is frequency
m1P = GPIO.PWM(m1pin1,50) #Motor 1 forward direction speed control
m1N = GPIO.PWM(m1pin2,50) #Motor 1 reverse direction speed control

#Motor 2 setup m2P -> 2, m2N -> 3, m3E -> 4
GPIO.setup(m2pin1,GPIO.OUT) #Input 3
GPIO.setup(m2pin2,GPIO.OUT) #Input 4

#PWM setup for motor 2
m2P = GPIO.PWM(m2pin1,50) #Motor 2 forward direction speed control
m2N = GPIO.PWM(m2pin2,50) #Motor 2 reverse direction speed control

#All Wheel Drive Forward, start 100% speed
#Consider Tutsplus for Truth table
#Code motor 1 and 2 overlap in order to match their RPM
GPIO.output(m1pin1,GPIO.LOW)  #Motor 1 - Input 1 set to High
GPIO.output(m1pin2,GPIO.HIGH) #Motor 2 - Input 3 set to High
GPIO.output(m2pin1,GPIO.HIGH)   #Motor 1 - Input 2 set to Low
GPIO.output(m2pin2,GPIO.LOW)  #Motor 2 - Input 4 set to Low

try:

        while 1:
                pass

except KeyboardInterrupt:
        GPIO.cleanup()



