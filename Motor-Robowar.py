#The code contains all the basic moving of the car such as:
#Forward, Backward, Rotate left and right
#This basic code will be combined with sensors to build the complete algorithm
import Rpi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #Consider the label of GPIO, not the pin number

#Motor 1 setup m1P -> 2, m1N -> 3, m1E -> 4
GPIO.setup(2,GPIO.OUT) #Input 1
GPIO.setup(3,GPIO.OUT) #Input 2
GPIO.setup(4,GPIO.OUT) #Enable 1,2

#PWM setup for motor 1, 50 is frequency
m1P = GPIO.PWM(2,50) #Motor 1 forward direction speed control
m1N = GPIO.PWM(3,50) #Motor 1 reverse direction speed control

#Motor 2 setup m2P -> 2, m2N -> 3, m3E -> 4
GPIO.setup(17,GPIO.OUT) #Input 3
GPIO.setup(22,GPIO.OUT) #Input 4
GPIO.setup(27,GPIO.OUT) #Enable 3,4

#PWM setup for motor 2
m2P = GPIO.PWM(2,50) #Motor 2 forward direction speed control
m2N = GPIO.PWM(3,50) #Motor 2 reverse direction speed control

#All Wheel Drive Forward, start 100% speed
#Consider Tutsplus for Truth table
#Code motor 1 and 2 overlap in order to match their RPM
pwm.start(100)
GPIO.output(2,GPIO.HIGH)  #Motor 1 - Input 1 set to High
GPIO.output(17,GPIO.HIGH) #Motor 2 - Input 3 set to High
GPIO.output(3,GPIO.LOW)   #Motor 1 - Input 2 set to Low
GPIO.output(22,GPIO.LOW)  #Motor 2 - Input 4 set to Low
GPIO.output(4,GPIO.HIGH)  #Motor 1 - Enable 1,2 set to High
GPIO.output(27,GPIO.HIGH) #Motor 2 - Enable 3,4 set to High

#All Wheel Drive Backward, start 100% speed
pwm.start(100)
GPIO.output(2,GPIO.LOW)   #Motor 1 - Input 1 set to Low
GPIO.output(17,GPIO.LOW)  #Motor 2 - Input 3 set to Low
GPIO.output(3,GPIO.HIGH)  #Motor 1 - Input 2 set to High
GPIO.output(22,GPIO.HIGH) #Motor 2 - Input 4 set to High
GPIO.output(4,GPIO.HIGH)  #Motor 1 - Enable 1,2 set to High
GPIO.output(27,GPIO.HIGH) #Motor 2 - Enable 3,4 set to High

#Robot rotates left with 100% speed
#Motor 2 is forward and position on the right
#Motor 1 is backward and position on the left
pwm.start(100)
GPIO.output(2,GPIO.LOW)   #Motor 1 - Input 1 set to Low
GPIO.output(17,GPIO.HIGH) #Motor 2 - Input 3 set to High
GPIO.output(3,GPIO.HIGH)  #Motor 1 - Input 2 set to High
GPIO.output(22,GPIO.LOW)  #Motor 2 - Input 4 set to Low
GPIO.output(4,GPIO.HIGH)  #Motor 1 - Enable 1,2 set to High
GPIO.output(27,GPIO.HIGH) #Motor 2 - Enable 3,4 set to High

#Robot rotates right with 100% speed
#Motor 1 is forward and position on the left
#Motor 2 is backward and position on the right
pwm.start(100)
GPIO.output(2,GPIO.HIGH)  #Motor 1 - Input 1 set to High
GPIO.output(17,GPIO.LOW)  #Motor 2 - Input 3 set to Low
GPIO.output(3,GPIO.LOW)   #Motor 1 - Input 2 set to Low
GPIO.output(22,GPIO.HIGH) #Motor 2 - Input 4 set to High
GPIO.output(4,GPIO.HIGH)  #Motor 1 - Enable 1,2 set to High
GPIO.output(27,GPIO.HIGH) #Motor 2 - Enable 3,4 set to High

#All Wheel Drive Forward Speed Control
#The speed control will be set to a specific range after our testing
#Replace m1P and m2P by m1N and m2N consecutively for reverse direction
for i in range(100):
        m1P.ChangeDutyCycle(i)
        m2P.ChangeDutyCycle(i)
        time.sleep(0.01)
        while i == 99:
            m1P.ChangeDutyCycle(i+1)
            m2P.ChangeDutyCycle(i+1)
            time.sleep(0.01)
            

