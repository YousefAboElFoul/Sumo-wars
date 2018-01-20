import RPi.GPIO as GPIO
import time

class QTR_8RC:
    """ Class for reading values from Pololu QT8-8RC sensor array.
    """
 
    def __init__(self):
        self.LEDON_PIN = 16
        self.SENSOR_PINS = [18]
        self.NUM_SENSORS = len(self.SENSOR_PINS)
        self.CHARGE_TIME = 10*1e-6 #10 us to charge the capacitors
        self.READING_TIMEOUT = 1e-3 #1 ms, assume reading is black

        self.sensorValues = [0] * self.NUM_SENSORS
        self.maxValue = 1e-3
        self.midValue = self.maxValue / 2


    def read_sensors(self):
        """ Follows the Pololu guidance for reading capacitor discharge/sensors:
            1. Set the I/O line to an output and drive it high.
            2. Allow at least 10 us for the sensor output to rise.
            3. Make the I/O line an input (high impedance).
            4. Measure the time for the voltage to decay by waiting for the I/O
                line to go low.
            Stores values in sensor values list, higher vals = darker surfaces.
        """
        for i in range(0, self.NUM_SENSORS):
            self.sensorValues[i] = self.READING_TIMEOUT

        for sensorPin in self.SENSOR_PINS:
            GPIO.setup(sensorPin, GPIO.OUT)
            GPIO.output(sensorPin, GPIO.HIGH)

        
        time.sleep(self.CHARGE_TIME)

        for sensorPin in self.SENSOR_PINS:
            #GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(sensorPin, GPIO.IN)


        startTime = time.clock()
        duration = 0
        while duration < self.READING_TIMEOUT:
            duration = time.clock() - startTime
            for i in range(0, self.NUM_SENSORS):
                if GPIO.input(self.SENSOR_PINS[i]) == 0 and duration < self.sensorValues[i]:
                    self.sensorValues[i] = duration

            
    def checkWhite (self):
        for i in range(0, self.NUM_SENSORS):
            if self.sensorValues[i] < self.midValue:
                return True
        return False

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BOARD)
        qtr = QTR_8RC()

        while 1:
            qtr.read_sensors()            

        
            if qtr.checkWhite():
                print ('white!')
            else:
                print ('black!')
        
	

    except KeyboardInterrupt:
        GPIO.cleanup()
