import RPi.GPIO as gpio
import time
from qtr_MCP import *

gpio.setwarnings(False)
        
line1Pins = [B0,B1,B2,B3,B4] #Forward left QTR
line2Pins = [A0] #Forward right QTR
line3Pins = [A2] #Back left QTR
line4Pins = [A3] #Back right QTR
ledPin1 = 16 
ledPin2 = 18
motor1FPin = 13 # Left motor input 1
motor1BPin = 15 # Left motor input 2
motor2FPin = 7 # Right motor input 1
motor2BPin = 11 # Right motor input 2


safetyDelay = 1 # For line detection before initiating rotation

gpio.setmode(gpio.BOARD)

#LED setup
gpio.setup(ledPin1, gpio.OUT)
gpio.setup(ledPin2, gpio.OUT)


#Motor 1 setup m1P -> 2, m1N -> 3
gpio.setup(motor1FPin,gpio.OUT) #Input 1
gpio.setup(motor1BPin,gpio.OUT) #Input 2

#Motor 2 setup m2P -> 2, m2N -> 3, m3E -> 4
gpio.setup(motor2FPin,gpio.OUT) #Input 3
gpio.setup(motor2BPin,gpio.OUT) #Input 4

#PWM setup for motor 1, 50 is frequency
m1F = gpio.PWM(motor1FPin,50) #Motor 1 forward direction speed control
m1B = gpio.PWM(motor1BPin,50) #Motor 1 reverse direction speed control

#PWM setup for motor 2
m2F = gpio.PWM(motor2FPin,50) #Motor 2 forward direction speed control
m2B = gpio.PWM(motor2BPin,50) #Motor 2 reverse direction speed control

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

#Rotate anti-clockwise with time 
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

        #For debugging
        qtr1.print_sensor_values()

        
        sensors = {'sen1': False, 'sen2': False, 'sen3': False, 'sen4': False}
        sensors['sen1'] = qtr1.checkWhite()
        sensors['sen2'] = qtr2.checkWhite()
        sensors['sen3'] = qtr3.checkWhite()
        sensors['sen4'] = qtr4.checkWhite()

     
        # Case 1: sensor 1 or sensor 2: Line detected front left and front right
        if sensors['sen1'] or sensors['sen2']:
                #LED activated to indicate sensor detection
                gpio.output(ledPin1, gpio.HIGH)
                #Brake and backup continiously as condition hold
                navigation(m1B, m2B, 100, 100)

                #Check again and perform extra backup for security
                startTime = time.time()
                duration = 0
                while duration < safetyDelay:
                        duration = time.time() - startTime
                        print (duration)
                        qtr1.read_sensors()
                        qtr2.read_sensors()
                        #For debugging
                        qtr1.print_sensor_values()
                        #Reset timer if white line was detected again
                        if qtr1.checkWhite() or qtr2.checkWhite():
                                startTime = time.time()


                #time.sleep(safetyDelay) #Backup and brake extra t second      
                gpio.output(ledPin1, gpio.LOW)
                    

        # Case 2: sensor 3 and sensor 4: Line detected back right and back left
        if sensors['sen3'] or sensors['sen4']:
                #LED activated to indicate sensor detection
                gpio.output(ledPin2, gpio.HIGH)
                #Moving forward continiously as condition hold
                navigation(m1F, m2F, 100, 100)
                #Check again and perform extra backup for security
                startTime = time.time()
                duration = 0
                while duration < safetyDelay:
                        duration = time.time() - startTime
                        print (duration)
                        qtr3.read_sensors()
                        qtr4.read_sensors()
                        #For debugging
                        qtr3.print_sensor_values()
                        #Reset timer if white line was detected again
                        if qtr3.checkWhite() or qtr4.checkWhite():
                                startTime = time.time()
                                
                #Check again and perform extra backup for security
                time.sleep(safetyDelay) #Backup and brake extra t second      
                gpio.output(ledPin2, gpio.LOW)


##        # Case 3: sensor 1 and sensor 3: Line detected front left & back right
##        # Think about being attacked by the enemy in this case, what should we do?
##        if sensors['sen1'] and sensors['sen3']:
##                Rotate_clockwise(2) #Rotate to change direction
##                navigation(m1F, m2F, 100, 100) #Moving away from white line
##                #Security check and perform forward in extra t second
##                if gpio.input(laserPin1) == False or gpio.input(laserPin3) == False:
##                        Forward(1) #Moving forward extra t second
##
##        # Case 3: sensor 1 and sensor 3: Line detected front left & back right
##        # Think about being attacked by the enemy in this case, what should we do?
##        if sensors['sen2'] and sensors['sen4']:
##                Rotate_anti_clockwise(2) #Rotate to change direction
##                navigation(m1F, m2F, 100, 100) #Moving away from white line
##                #Security check and perform forward in extra t second
##                if gpio.input(laserPin2) == False or gpio.input(laserPin4) == False:
##                        Forward(1) #Moving forward extra t second



if __name__ == "__main__":
    try:
        qtr1 = QTR_8RC(line1Pins)
        qtr2 = QTR_8RC(line2Pins)
        qtr3 = QTR_8RC(line3Pins)
        qtr4 = QTR_8RC(line4Pins)

        print ("press CTRL + C to exit")

        while 1:
                lineDetector(qtr1,qtr2,qtr3,qtr4)     
                navigation(m1F, m2F, 100, 100)

    except KeyboardInterrupt:
        gpio.cleanup()
