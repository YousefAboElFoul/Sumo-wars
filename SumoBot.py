import time
from qtr_MCP import *
from qtr import *

gpio.setwarnings(False)

qtrFL = None #Forward left QTR
qtrFR = None #Forward right QTR
qtrB = None  #Back QTR
qtrFLPins = [B0,B1,B2,B3,B4,B5,B6,B7] #Forward left QTR
qtrFRPins = [A0,A1,A2,A3,A4,A5,A6,A7] #Forward right QTR
qtrBPins = [36,38,40] #Back left QTR
ledPin1 = 16    #Used for debugging line sensors
ledPin2 = 18    #Used for debugging line sensors
motor1FPin = 31 # Left motor input 1
motor1BPin = 33 # Left motor input 2
motor2FPin = 37 # Right motor input 1
motor2BPin = 35 # Right motor input 2
GPIO_TRIGGER = 22 # Ultrasonic pin
GPIO_ECHO = 24
switchPin = 7
rotatetime = 0.5
curState = False # used for initial switch
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
##def navigation (mode1, mode2, dc1, dc2):
##        mode1.ChangeDutyCycle(dc1)
##        mode2.ChangeDutyCycle(dc2)
##        time.sleep(0.01)

def navigation (mode1a, mode1b,mode2a, mode2b):
        gpio.output(motor1FPin,mode1a)  
        gpio.output(motor1BPin,mode1b)  
        gpio.output(motor2FPin,mode2a)  
        gpio.output(motor2BPin,mode2b)  
  
# Both motors push forward
def forward():
        navigation(1,0,1,0)
        
# Both motors push backward     
def backward():
        navigation(0,1,0,1)
        
# Rotate clockwise
def rotateCW():
        navigation(1, 0, 0, 1)

# Rotate counter clockwise
def rotateCCW():
        navigation(0, 1, 1, 0)
          
def lineDetector():
        #global thread1
        
        qtrFL.read_sensors()            
        qtrFR.read_sensors()
        qtrB.read_sensors()

        #For debugging
        qtrB.print_sensor_values()

        sensors = {'sen1': False, 'sen2': False, 'sen3': False}
        sensors['sen1'] = qtrFL.checkWhite()
        sensors['sen2'] = qtrFR.checkWhite()
        sensors['sen3'] = qtrB.checkWhite()

     
        # Case 1: sensor 1 or sensor 2: Line detected front left and front right
        if sensors['sen1'] or sensors['sen2']:
                #LED activated to indicate sensor detection
                gpio.output(ledPin1, gpio.HIGH)
                #Backup continiously as condition hold
                backward()
                #Check again and perform extra backup for security
                startTime = time.time()
                while time.time() - startTime < safetyDelay:
                        qtrFL.read_sensors()
                        qtrFR.read_sensors()
                        #For debugging
                        qtrFL.print_sensor_values()
                        #Reset timer if white line was detected again
                        if qtrFL.checkWhite() or qtrFR.checkWhite():
                                startTime = time.time()

                gpio.output(ledPin1, gpio.LOW)

        # Case 2: sensor 3: Line detected back right and back left
        if sensors['sen3']:
                #LED activated to indicate sensor detection
                gpio.output(ledPin2, gpio.HIGH)
                #Moving forward continiously as condition hold
                forward()
                #Check again and perform extra backup for security
                startTime = time.time()
                while time.time() - startTime < safetyDelay:
                        qtrB.read_sensors()
                        #For debugging
                        qtrB.print_sensor_values()
                        #Reset timer if white line was detected again
                        if qtrB.checkWhite():
                                startTime = time.time()
                                
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


########################object detection##########################

def distance():
        # set Trigger to HIGH
        gpio.output(GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        gpio.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while gpio.input(GPIO_ECHO) == 0:
                StartTime = time.time()

        # save time of arrival
        while gpio.input(GPIO_ECHO) == 1:
                StopTime = time.time()
        
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cms)
        # and divide by 2, because there and back
        distance = (TimeElapsed*34300)/2

        return distance
#######################################################
def detectobj():
        dist = distance()
        print (dist)
        # No reasonable distance has been detected
        while dist>1000 or dist==0:
                rotateCW()
                time.sleep(rotatetime)
                dist=distance()                               

        # Attack the detected object
        forward()


################################################
if __name__ == "__main__":
    try:
        qtrFL = QTR_MCP(qtrFLPins)
        qtrFR = QTR_MCP(qtrFRPins)
        qtrB = QTR(qtrBPins)

        gpio.setup(GPIO_TRIGGER,gpio.OUT)
        gpio.setup(GPIO_ECHO,gpio.IN)
        gpio.setup(switchPin,gpio.IN)
        
        print ("press CTRL + C to exit")

        #time - for - no echo
        detectTime = time.time()
        
        while 1:
                if gpio.input(switchPin) == 1 and curState == False:
                        time.sleep(3)
                        curState = True

                elif gpio.input(switchPin) == 0 and curState == True:
                        curState = False
                        
                while gpio.input(switchPin) == 1 and curState == True:
                        lineDetector()     
                        
    except KeyboardInterrupt:
        gpio.cleanup()
