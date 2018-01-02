import RPi.GPIO as GPIO
import time

laserPin1 = 14 # Front left sensor
laserPin2 = 15 # Front right sensor
laserPin3 = 18 # Back left sensor
laserPin4 = 24 # Back right sensor
ledPin1 = 23 
ledPin2 = 25 
ledPin3 = 25
ledPin4 = 25
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
	
	# Case 1: Line detected front left
	# Do: - BW+CW - left motor FW - right motor BW - LED 1 High
    if not GPIO.input(laserPin1):
		GPIO.output(ledPin4, GPIO.LOW)
        GPIO.output(ledPin1, GPIO.HIGH)
		navigation (m1B,m2B,100,100)	
		# Continue going BWD while the sensor is still seeing the line			
		while not GPIO.input(laserPin1):
			#None
		# Go BWD extra time for safety
		time.sleep(safetyDelay)
		navigation (m1F,m2B,100,100)
		
	# Case 2: Line detected back right
	# Do: - FW+CCW - left motor BW - right motor FW - LED 4 High	
	elif not GPIO.input(laserPin4):
		GPIO.output(ledPin1, GPIO.LOW)
		GPIO.output(ledPin4, GPIO.HIGH)
		navigation (m1F,m2F,100,100)	
		# Continue going FWD while the sensor is still seeing the line			
		while not GPIO.input(laserPin4):
			#None
		# Go FWD for extra time for safety
		time.sleep(safetyDelay)
		navigation (m1B,m2F,100,100)

	# Case 3: Line detected front right
	# Do: - BW+CCW - left motor BW - right motor FW - LED 1 High
    if not GPIO.input(laserPin2):
		GPIO.output(ledPin3, GPIO.LOW)
		GPIO.output(ledPin2, GPIO.HIGH)
		navigation (m1B,m2B,100,100)	
		# Continue going BWD while the sensor is still seeing the line			
		while not GPIO.input(laserPin2):
			#None
		# Go BWD for extra time for safety
		time.sleep(safetyDelay)
		navigation (m1B,m2F,100,100)
		
	# Case 4: Line detected back left
	# Do: - FW+CW - left motor FW - right motor BW - LED 3 High
	elif not GPIO.input(laserPin3):
		GPIO.output(ledPin2, GPIO.LOW)
		GPIO.output(ledPin3, GPIO.HIGH)
		navigation (m1F,m2F,100,100)	
		# Continue going FWD while the sensor is still seeing the line			
		while not GPIO.input(laserPin3):
			#None
		# Go FWD for extra time for safety
		time.sleep(safetyDelay)
		navigation (m1F,m2B,100,100)
	

GPIO.setmode(GPIO.BCM)

GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)

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



