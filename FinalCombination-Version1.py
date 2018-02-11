#Please have a look guys since there is a lot of changes in this code.
#The content of the code still the same, just the way of coding is changed.
#I think this change has optimized our code and made it simpler.
#Let me know your guys opinions and we will continue to discuss during our meeting
#Thank you!!!!
import RPi.GPIO as GPIO
import time
from qtr import *


line1Pins = [18]
line2Pins = [24]
line3Pins = [26]
line4Pins = [32]
ledPin1 = 16 
ledPin2 = 22 
ledPin3 = 22
ledPin4 = 22
motor1FPin = 3 # Left motor input 1
motor1BPin = 5 # Left motor input 2
motor2FPin = 7 # Right motor input 1
motor2BPin = 11 # Right motor input 2


safetyDelay = 1 # For line detection before initiating rotation

GPIO.setmode(GPIO.BOARD)

#LED setup
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)


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
          
def lineDetector(qtr1,qtr2,qtr3,qtr4):
        qtr1.read_sensors()            
        qtr2.read_sensors()
        qtr3.read_sensors()
        qtr4.read_sensors()

        
        sensors = {'sen1': False, 'sen2': False, 'sen3': False, 'sen4': False}
        sensors['sen1'] = qtr1.checkWhite()
        sensors['sen2'] = qtr2.checkWhite()
        sensors['sen3'] = qtr3.checkWhite()
        sensors['sen4'] = qtr4.checkWhite()

     
        # Case 1: sensor 1 or sensor 2: Line detected front left and front right
        if sensors['sen1'] or sensors['sen2']:
                #LED activated to indicate sensor detection
                GPIO.output(ledPin1, GPIO.HIGH)
                #Brake and backup continiously as condition hold
                navigation(m1B, m2B, 100, 100)
                while qtr1.checkWhite() or qtr2.checkWhite():
                        qtr1.read_sensors()
                        qtr2.read_sensors()

                #Check again and perform extra backup for security
                time.sleep(safetyDelay) #Backup and brake extra t second      
                GPIO.output(ledPin1, GPIO.LOW)
                    

        # Case 2: sensor 3 and sensor 4: Line detected back right and back left
        if sensors['sen3'] or sensors['sen4']:
                #LED activated to indicate sensor detection
                GPIO.output(ledPin2, GPIO.HIGH)
                #Moving forward continiously as condition hold
                navigation(m1F, m2F, 100, 100)
                while qtr3.checkWhite() or qtr4.checkWhite():
                        qtr3.read_sensors()
                        qtr4.read_sensors()
                #Check again and perform extra backup for security
                time.sleep(safetyDelay) #Backup and brake extra t second      
                GPIO.output(ledPin2, GPIO.LOW)


##        # Case 3: sensor 1 and sensor 3: Line detected front left & back right
##        # Think about being attacked by the enemy in this case, what should we do?
##        if sensors['sen1'] and sensors['sen3']:
##                Rotate_clockwise(2) #Rotate to change direction
##                navigation(m1F, m2F, 100, 100) #Moving away from white line
##                #Security check and perform forward in extra t second
##                if GPIO.input(laserPin1) == False or GPIO.input(laserPin3) == False:
##                        Forward(1) #Moving forward extra t second
##
##        # Case 3: sensor 1 and sensor 3: Line detected front left & back right
##        # Think about being attacked by the enemy in this case, what should we do?
##        if sensors['sen2'] and sensors['sen4']:
##                Rotate_anti_clockwise(2) #Rotate to change direction
##                navigation(m1F, m2F, 100, 100) #Moving away from white line
##                #Security check and perform forward in extra t second
##                if GPIO.input(laserPin2) == False or GPIO.input(laserPin4) == False:
##                        Forward(1) #Moving forward extra t second



if __name__ == "__main__":
    try:
        qtr1 = QTR_8RC(line1Pins)
        qtr2 = QTR_8RC(line2Pins)
        qtr3 = QTR_8RC(line3Pins)
        qtr4 = QTR_8RC(line4Pins)

        print ("press CTRL + C to exit")

        while 1:
            
            #qtr.print_sensor_values()
        
                lineDetector(qtr1,qtr2,qtr3,qtr4)     
                navigation(m1F, m2F, 100, 100)

    except KeyboardInterrupt:
        GPIO.cleanup()
