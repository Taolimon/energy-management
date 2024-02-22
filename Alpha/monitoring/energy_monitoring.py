import numbers
import time
import math
import csv

sensorReadingFormat = ["Date", "Time", "Name", "Value"]
usingDirectReadings = False

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

    # Check if using readings or estimates
    if usingDirectReadings:
        current_reading = getEnergyStream(energyStream)
    else:
        pass

    # Store the readings in a file
    #storeReading(current_reading)
    return

main()