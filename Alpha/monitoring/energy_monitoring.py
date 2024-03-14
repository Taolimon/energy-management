import numbers
import time
import math
import csv
import RPi.GPIO as GPIO
import smbus

sensorReadingFormat = ["Date", "Time", "Name", "Value"]
usingDirectReadings = False

# GPIO Global Variables
GPIO.setmode(GPIO.BCM)
pir_gpio = 14
digital_light_gpio = 27
GPIO.setup(pir_gpio, GPIO.IN)
GPIO.setup(digital_light_gpio, GPIO.IN)

### BH1750 I2C Light Sensor Variables
# These variables include the adresses and various light intesnity thresholds
# Addresses
# BH1750_ADDR - the adress used by the sensor on the i2c bus
BH1750_ADDR = 0x23
CONTINUOUS_HIGH_RESOLUTION_MODE = 0x10
# Light Intensity Thresholds
# ARTIFICIAL_LIGHT_THRESHOLD - the average light intensity of artificial light
# The average light intensity of daylight in the evenings, early afternoon, late_afternoon, morning and nights
ARTIFICIAL_LIGHT_THRESHOLD = 150.0
EVENING_DAYLIGHT_ = 3.4
LATE_AFTERNOON_DAYLIGHT = 3.4
EARLY_AFTERNOON_DAYLIGHT = 20.0
MORNING_DAYLIGHT = 25.0
NIGHT = 0.0

class lightState():
    lightStates = ["OnFromPIR", "OffFromPIR", "OnFromElse", "OffFromElse"]

    def __init__(self, state) -> None:
        self.currentLightState = state

    def getState(self):
        return self.currentLightState

    def changeState(self, new_state):
        self.currentLightState = new_state

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

def changeLightState(lstate, pir_r, light_r, threshold):
    if (pir_r == False):
        return False
    elif (light_r >= ARTIFICIAL_LIGHT_THRESHOLD):
        lstate.changeState("OnFromElse")
        return False
    else:
        if (light_r >= threshold):
            if (lstate.getState() == "OffFromElse" or lstate.getState() == "OffFromPIR"):
                lstate.changeState("OnFromPIR")
                return True
    return False

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
    starting_time = time.time()
    max_reading_time = 15

    try:
        while True:
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
                    return True
                time.sleep(1)
            time.sleep(1)

            ct = time.time()
            td = ct - starting_time
            if (sensor_counter >= max_counter or td >= max_reading_time):
                sensor_counter = 0
                return False

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

# BH1750 Light Intensity Sensor
def checkBH1750(bus):
    data = bus.read_i2c_block_data(BH1750_ADDR, CONTINUOUS_HIGH_RESOLUTION_MODE)
    light_intensity = (data[1] + (256 * data[0])) / 1.2
    print("Light_Intensity: ", light_intensity)
    return light_intensity

# General Sensors
def checkSensors(bus):
    checkBH1750(bus)
    readPIRSensor()

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

def checkCurrentTime():
    current_hour = time.strftime("%H")
    current_hour = int(current_hour)
    daylight_hour = None
    if (current_hour >= 6 and current_hour < 12 ):
        daylight_hour = MORNING_DAYLIGHT
    elif (current_hour >= 12 and current_hour < 15):
        daylight_hour = EARLY_AFTERNOON_DAYLIGHT
    elif (current_hour >= 15 and current_hour < 18):
        daylight_hour = LATE_AFTERNOON_DAYLIGHT
    elif (current_hour >= 18 and current_hour < 21):
        daylight_hour = EVENING_DAYLIGHT_
    else:
        daylight_hour = NIGHT
    return daylight_hour

def main():
    # Variables
    ListOfReadings = []
    energyStream = 0 ### Find a way to get the energy stream
    light2x26pl_c_concord = lightingEstimate("2 x 26w pl-c concord round recessed fittings", 26)
    light2x26Marlin = lightingEstimate("2 x 26w Marlin round surface bulkhead", 26)
    bus = smbus.SMBus(1)
    bus.write_byte(BH1750_ADDR, CONTINUOUS_HIGH_RESOLUTION_MODE)

    # check the current time to get the apropriate light threshold
    light_threshold = checkCurrentTime()

    if (checkBH1750(bus) >= ARTIFICIAL_LIGHT_THRESHOLD):
        stateOfLights = lightState("OnFromElse")
    else:
        stateOfLights = lightState("OffFromElse")

    # Check if using readings or estimates
    if usingDirectReadings:
        current_reading = getEnergyStream(energyStream)
    else:
        pass

    while True:
        pir_reading = readPIRSensor()
        bh1750_reading = checkBH1750(bus)

        print("pir_reading: " + str(pir_reading))
        print("bh1750_reading: " + str(bh1750_reading))
        time.sleep(2)
        print("\n")

        stateChangeStatus = changeLightState(stateOfLights, pir_reading, bh1750_reading, light_threshold)
        print("Light State: ", stateOfLights.getState())

    # Store the readings in a file
    #storeReading(current_reading)
    return

main()