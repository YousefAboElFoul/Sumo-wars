#Please have a look guys since there is a lot of changes in this code.
#The content of the code still the same, just the way of coding is changed.
#I think this change has optimized our code and made it simpler.
#Let me know your guys opinions and we will continue to discuss during our meeting
#Thank you!!!!
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

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

#LED setup
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)

#Line Detector sensors setup
GPIO.setup(laserPin1, GPIO.IN)
GPIO.setup(laserPin2, GPIO.IN)
GPIO.setup(laserPin3, GPIO.IN)
GPIO.setup(laserPin4, GPIO.IN)

#Motor 1 setup m1P -> 2, m1N -> 3
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

# Controls the motors setting
def navigation (mode1, mode2, dc1, dc2):
        mode1.ChangeDutyCycle(dc1)
        mode2.ChangeDutyCycle(dc2)
        time.sleep(0.01)
        
def B_brake(t):
	counter = 0
	while counter != t:
                time.sleep(1)
		counter += 1
		nav(m1B, m2B, 100, 100) #Moving backward

#Forward in t seconds
def Forward(t):
	counter = 0
	while counter != t:
		time.sleep(1)
		counter += 1
		nav(m1F, m2F, 100, 100) #Moving Forward

#Rotate clockwise with time t
def Rotate_clockwise(t):
	counter = 0
	while counter != t:
		time.sleep(1)
		counter += 1
		nav(m1F, m2B, 100, 100) #Rotate

#Rotate anti-clockwise with time t
def Rotate_anti_clockwise(t):
	counter = 0
	while counter != t:
		time.sleep(1)
		counter += 1
		nav(m1B, m2F, 100, 100) #Rotate
		
# Returns a dictionary with keys set to TRUE if the corresponding sensor detected white line 
def lineDetector():
	# Case 1: sensor 1 and sensor 2: Line detected front left and front right
	while not GPIO.input(laserPin1) or not GPIO.input(laserPin2):
            #LED activated to indicate sensor detection
            GPIO.output(ledPin1, GPIO.LOW)
            GPIO.output(ledPin2, GPIO.HIGH)
            #Brake and backup continiously as condition hold
            navigation(m1B, m2B, 100, 100)
            #Check again and perform extra backup for security
            if GPIO.input(laserPin1) == False or GPIO.input(laserPin2) == False:
                B_brake(1) #Backup and brake extra t second                

	# Case 2: sensor 3 and sensor 4: Line detected back right and back left
	while not GPIO.input(laserPin3) or not GPIO.input(laserPin4):
            #LED activated to indicate sensor detection
            if not GPIO.input(laserPin3):
                GPIO.output(ledPin3, GPIO.HIGH)
            if not GPIO.input(laserPin4):
                GPIO.output(ledPin4, GPIO.HIGH)
            #Moving forward continiously as condition hold
            navigation(m1F, m2F, 100, 100)
            #Check again and perform extra backup for security
            #We might have a brake here. Will decide through testing.
            if GPIO.input(laserPin3) == False or GPIO.input(laserPin4) == False:
                Forward(1) #Moving forward extra t second

        # Case 3: sensor 1 and sensor 3: Line detected front left & back right
        # Think about being attacked by the enemy in this case, what should we do?
        while not GPIO.input(laserPin1) and not GPIO.input(laserPin3):
            Rotate_clockwise(2) #Rotate to change direction
            navigation(m1F, m2F, 100, 100) #Moving away from white line
            #Security check and perform forward in extra t second
            if GPIO.input(laserPin1) == False or GPIO.input(laserPin3) == False:
                Forward(1) #Moving forward extra t second

        # Case 3: sensor 1 and sensor 3: Line detected front left & back right
        # Think about being attacked by the enemy in this case, what should we do?
        while not GPIO.input(laserPin2) and not GPIO.input(laserPin4):
            Rotate_anti_clockwise(2) #Rotate to change direction
            navigation(m1F, m2F, 100, 100) #Moving away from white line
            #Security check and perform forward in extra t second
            if GPIO.input(laserPin2) == False or GPIO.input(laserPin4) == False:
                Forward(1) #Moving forward extra t second


print ("press CTRL + C to exit")

try:
    while 1:
        #Switch on, Line detector activate, then rotate to scan enemy
        lineDetector()
        navigation(m1F, m2B, 100, 100) #Rotate to scan enemy
        #while detected():
            #lineDetector() # 1st priority
            #attack() #2nd priority
		
except KeyboardInterrupt:
    GPIO.cleanup()



