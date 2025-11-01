# lineFollowSensorTest.py

# Created by Colin Adreani on 10/25/2025

from basehat import LineFinder
import time

# set the pin to be used
pinL = 5
pinR = 5

# Initializing the sensor so the function within the class can be used
lineSensorL = lineFinder(pinL)
lineSensorR = lineFinder(pinR)

try:
  while True:
    lineL = lineSensorL.value
    lineR = lineSensorR.value

    print(f'\n Right Line = {lineL}, Left Line = {lineR}')

    rSpeed = 30 if lineR else 70
    lSpeed = 30 if lineL else 70

    print(f'rSpeed = {rSpeed}, lSpeed = {lSpeed}')

    time.sleep(0.05)
except KeyboardInterrupt:
  print("\nCtrl+C detected. Exiting...")