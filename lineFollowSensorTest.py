# lineFollowSensorTest.py

# Created by Colin Adreani on 10/25/2025

from basehat import LineFinder, ColorSensor
import time

# set the pin to be used
pinL = 5
pinC = 'C'

# Initializing the sensor so the function within the class can be used
lineSensor = lineFinder(pinL)
colorSensor = ColorSensor(pinC)

try:
  while True:
    line = lineSensor.value
    color = colorSensor.get_color_hsv()

    print(f'\ndiffL = {line} ---- diffR = {color}')

    rSpeed = 30 if line else 70
    lSpeed = 30 if line else 70

    print(f'rSpeed = {rSpeed}, lSpeed = {lSpeed}')

    time.sleep(0.05)
except KeyboardInterrupt:
  print("\nCtrl+C detected. Exiting...")