import RPi.GPIO as GPIO
import time

def lineDetector():
    sensors = {'sen1' : False, 'sen2' : False,'sen3' : False,'sen4' : False}
    if not GPIO.input(laserPin1):
        sensors['sen1'] = True;
    if not GPIO.input(laserPin2):
        sensors['sen2'] = True;

    return sensors

laserPin1 = 18 # (BCM)
laserPin2 = 24 # (BCM)
laserPin3 = 18 # (BCM)
laserPin4 = 18 # (BCM)
ledPin1 = 23 # (BCM)
ledPin2 = 25 # (BCM)


GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)
GPIO.setup(laserPin1, GPIO.IN)
GPIO.setup(laserPin2, GPIO.IN)

print ("press CTRL + C to exit")

try:
    while 1:
        sensors = lineDetector()
        if sensors['sen1']:
            GPIO.output(ledPin1, GPIO.HIGH)

        else:
            GPIO.output(ledPin1, GPIO.LOW)

        if sensors['sen2']:
            GPIO.output(ledPin2, GPIO.HIGH)

        else:
            GPIO.output(ledPin2, GPIO.LOW)


except KeyboardInterrupt:
    GPIO.cleanup()



