#The code contains all the basic moving of the car such as:
#Forward, Backward, Rotate left and right
#This basic code will be combined with sensors to build the complete algorithm
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD) #Consider the label of GPIO, not the pin number

motor1FPin=31
motor1BPin=33

motor2FPin=37
motor2BPin=35

def navigation (mode1a, mode1b,mode2a, mode2b):
        GPIO.output(motor1FPin,mode1a)  
        GPIO.output(motor1BPin,mode1b)  
        GPIO.output(motor2FPin,mode2a)  
        GPIO.output(motor2BPin,mode2b)

#Motor 1 setup m1P -> 2, m1N -> 3, m1E -> 4
GPIO.setup(motor1FPin,GPIO.OUT) #Input 1
GPIO.setup(motor1BPin,GPIO.OUT) #Input 2

#PWM setup for motor 1, 50 is frequency
m1P = GPIO.PWM(motor1FPin,50) #Motor 1 forward direction speed control
m1N = GPIO.PWM(motor1BPin,50) #Motor 1 reverse direction speed control

#Motor 2 setup m2P -> 2, m2N -> 3, m3E -> 4
GPIO.setup(motor2FPin,GPIO.OUT) #Input 3
GPIO.setup(motor2BPin,GPIO.OUT) #Input 4

#PWM setup for motor 2
m2P = GPIO.PWM(motor2FPin,50) #Motor 2 forward direction speed control
m2N = GPIO.PWM(motor2BPin,50) #Motor 2 reverse direction speed control


try:

        while 1:
                navigation (1,0,0,1)
                time.sleep (0.5)
                navigation (0,0,0,0)
                time.sleep (0.5)

except KeyboardInterrupt:
        GPIO.cleanup()



