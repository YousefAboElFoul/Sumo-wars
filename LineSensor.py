import RPi.GPIO as GPIO
import time

laserPin1 = 18 # Front left sensor
laserPin2 = 24 # Front right sensor
laserPin3 = 24 # Back left sensor
laserPin4 = 24 # Back right sensor
ledPin1 = 25 
ledPin2 = 21 
ledPin3 = 16
ledPin4 = 23
motor1FPin = 2	# Left motor input 1
motor1BPin = 3	# Left motor input 2
motor2FPin = 17 # Right motor input 1
motor2BPin = 22 # Right motor input 2

safetyDelay = 1 # For line detection before initiating rotation

# Controls the motors setting
def navigation (mode1, mode2, dc1, dc2):
        mode1.ChangeDutyCycle(dc1)
        mode2.ChangeDutyCycle(dc2)
        time.sleep(0.01)

# Returns a dictionary with keys set to TRUE if the corresponding sensor detected white line 
def lineDetector():
        #print (GPIO.input(laserPin4))

	
	# Case 1: Line detected front left
	# Do: - BW+CW - left motor FW - right motor BW - LED 1 High
	if not GPIO.input(laserPin1):
                GPIO.output(ledPin1, GPIO.HIGH)
                navigation (m1B,m2B,100,100)	
                # Continue going BWD while the sensor is still seeing the line			
                while not GPIO.input(laserPin1):
                        pass
                # Go BWD extra time for safety
                time.sleep(safetyDelay)
                navigation (m1F,m2B,100,100)
                GPIO.output(ledPin1, GPIO.LOW)


	# Case 2: Line detected back right
	# Do: - FW+CCW - left motor BW - right motor FW - LED 4 High	
	elif not GPIO.input(laserPin4):
                GPIO.output(ledPin4, GPIO.HIGH)
                navigation (m1F,m2F,100,100)	
                # Continue going FWD while the sensor is still seeing the line			
                while not GPIO.input(laserPin4):
                        pass
                # Go FWD for extra time for safety
                time.sleep(safetyDelay)
                navigation (m1B,m2F,100,100)
                GPIO.output(ledPin4, GPIO.LOW)


	# Case 3: Line detected front right
	# Do: - BW+CCW - left motor BW - right motor FW - LED 1 High
	if not GPIO.input(laserPin2):
                GPIO.output(ledPin2, GPIO.HIGH)
                navigation (m1B,m2B,100,100)	
                # Continue going BWD while the sensor is still seeing the line			
                while not GPIO.input(laserPin2):
                        pass
                # Go BWD for extra time for safety
                time.sleep(safetyDelay)
                navigation (m1B,m2F,100,100)
                GPIO.output(ledPin2, GPIO.LOW)


	# Case 4: Line detected back left
	# Do: - FW+CW - left motor FW - right motor BW - LED 3 High
	elif not GPIO.input(laserPin3):
                GPIO.output(ledPin3, GPIO.HIGH)
                navigation (m1F,m2F,100,100)	
                # Continue going FWD while the sensor is still seeing the line			
                while not GPIO.input(laserPin3):
                        pass
                # Go FWD for extra time for safety
                time.sleep(safetyDelay)
                navigation (m1F,m2B,100,100)
                GPIO.output(ledPin3, GPIO.LOW)


GPIO.setmode(GPIO.BCM)

GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)
GPIO.setup(ledPin3, GPIO.OUT)
GPIO.setup(ledPin4, GPIO.OUT)


#Line Detector sensors setup
GPIO.setup(laserPin1, GPIO.IN)
GPIO.setup(laserPin2, GPIO.IN)
GPIO.setup(laserPin3, GPIO.IN)
GPIO.setup(laserPin4, GPIO.IN)

#Motor 1 setup m1P -> 2, m1N -> 3, m1E -> 4
GPIO.setup(motor1FPin,GPIO.OUT) #Input 1
GPIO.setup(motor1BPin,GPIO.OUT) #Input 2

#Motor 2 setup m2P -> 2, m2N -> 3, m3E -> 4
GPIO.setup(motor2FPin,GPIO.OUT) #Input 3
GPIO.setup(motor2BPin,GPIO.OUT) #Input 4

#PWM setup for motor 1, 50 is frequency
m1F = GPIO.PWM(motor1FPin,50) #Motor 1 forward direction speed control
m1B = GPIO.PWM(motor1BPin,50) #Motor 1 reverse direction speed control

#PWM setup for motor 2
m2F = GPIO.PWM(motor2FPin,50) #Motor 2 forward direction speed control
m2B = GPIO.PWM(motor2BPin,50) #Motor 2 reverse direction speed control

print ("press CTRL + C to exit")

try:
    while 1:
        lineDetector()
		
except KeyboardInterrupt:
    GPIO.cleanup()



