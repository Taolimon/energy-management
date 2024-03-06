import numbers
import time
import math
import csv
import RPi.GPIO as GPIO

sensorReadingFormat = ["Date", "Time", "Name", "Value"]
usingDirectReadings = False

# GPIO Global Variables
GPIO.setmode(GPIO.BCM)
pir_gpio = 14
digital_light_gpio = 27
GPIO.setup(pir_gpio, GPIO.IN)
GPIO.setup(digital_light_gpio, GPIO.IN)

class lightState():
    lightStates = ["OnFromPIR", "OffFromPIR", "OnFromElse", "OffFromElse"]

    def __init__(self, state) -> None:
        self.currentLightState = state

class lightingEstimate():
    def __init__(self, name, watts) -> None:
        self.name = name
        self.watts = watts

class sensorReading():
    def __init__(self, date, time, name, value) -> None:
        self.date = date
        self.name = name
        self.time = time
        self.value = value

    def updateValue(self, newValue):
        self.value = newValue

class readingsList():
    sensorReadings = []

    def addReading(self, reading):
        self.sensorReadings.append(reading)

# PIR Sensor        
def prepareSensor():
    print("Preparing the PIR Module")
    time.sleep(2)
    return

def readPIRSensor():
    # Add a counter and timer to see if there's multiple movement in quick succession
    # This is because for every 3 undetected readings, there's a false positive
    sensor_counter = 0
    max_counter = 2
    max_time_difference = 5

    try:
        while True:

            checkDLightSensor()

            if (GPIO.input(pir_gpio) == 0):
                print("No sensor data")
            elif (GPIO.input(pir_gpio) == 1):
                print("Motion Detected")
                sensor_counter += 1
                if sensor_counter == 1:
                    detecting_time = time.time()
                current_time = time.time()
                time_difference = current_time - detecting_time
                #print(current_time)
                #print(detecting_time)
                print("time passed since last detection: " + str(time_difference))
                if (sensor_counter >= max_counter and time_difference <= max_time_difference):
                    print("sufficient motion detected.")
                    detecting_time = time.time()
                    current_time = time.time()
                time.sleep(1)
            time.sleep(1)
        
            if (sensor_counter >= max_counter):
                sensor_counter = 0

    except KeyboardInterrupt:
        print('\ninterrupted')
        GPIO.cleanup()
        return
    
# Digital Light Sensor
def checkDLightSensor():
    if(GPIO.input(digital_light_gpio) == 1):
        print("Digital Light Sensor: No data")
    else:
        print("Digital Light Sensor: Light Detected")
    return

# Energy Stream
def getEnergyStream(energyStream):
    if energyStream == None:
        return
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S",t)

    # incomplete energy_average should take in the mean of the energyStream as
    # energyStream/time
    energy_average = energyStream
    return energy_average

def storeReading(energyReading):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S",t)
    current_date = time.strftime("%z %Y-%m-%d", t)
    current_month = time.strftime("%M")
    newReading = sensorReading(current_date, current_time, "current_reading", energyReading)

    with open(current_month + "/sensor_readings.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(sensorReadingFormat)
        writer.writerow([newReading.date, newReading.time, newReading.name, newReading.value])

def main():
    # Variables
    ListOfReadings = []
    energyStream = 0 ### Find a way to get the energy stream
    light2x26pl_c_concord = lightingEstimate("2 x 26w pl-c concord round recessed fittings", 26)
    light2x26Marlin = lightingEstimate("2 x 26w Marlin round surface bulkhead", 26)
    stateOfLights = lightState("OffFromElse")

    # Check if using readings or estimates
    if usingDirectReadings:
        current_reading = getEnergyStream(energyStream)
    else:
        pass

    readPIRSensor()

    # Store the readings in a file
    #storeReading(current_reading)
    return

main()
