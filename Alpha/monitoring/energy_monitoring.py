import numbers
import time
import math

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
    newReading = sensorReading(current_date, current_time, "current_reading", energyReading)

def main():
    ListOfReadings = []
    energyStream = 0 ### Find a way to get the energy stream
    current_reading = getEnergyStream(energyStream)
    storeReading(current_reading)
    return

main()