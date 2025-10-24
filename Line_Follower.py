# Line_Follower.py

# Created by Colin Adreani on 10/20/2025


# More info and instruction on using this sensor can be found in the basehat folder
# on your Pi's Desktop 

from basehat import LightSensor, UltrasonicSensor
from buildhat import Motor
import time

# uPin = 5

motorL = Motor('A')
motorR = Motor('B')

# ultra = UltrasonicSensor(uPin)

def drive(rSpeed, lSpeed, time):
  motorR.start(rSpeed)
  motorL.start(-lSpeed)

  time.sleep(time/1000)

  motorR.stop()
  motorL.stop()

def driveStart(rSpeed, lSpeed):
  motorR.start(rSpeed)
  motorL.start(-lSpeed)

def stop():
  motorR.stop()
  motorL.stop()

def main():
  # set the pin to be used
  pinL = 0
  pinR = 0

  # Initializing the sensor so the function within the class can be used
  lightSensorL = LightSensor(pinL)
  lightSensorR = LightSensor(pinR)

  lightL = lightSensorL.light
  lightR = lightSensorR.light

  avgL = 0;
  avgR = 0;

  for i in range(0,100):
    lightL = lightSensorL.light
    lightR = lightSensorR.light

    avgL += lightL
    avgR += lightR

    time.sleep(0.01)
  
  avgL = avgL/100
  avgR = avgR/100

  try: 
    while True:
      try: 
        lightL = lightSensorL.light
        lightR = lightSensorR.light
        print(f'avgL = {avgL}, curL = {lightL}')
        print(f'avgR = {avgR}, curR = {lightR}')

        # update and read the values of the lineFinder
        lightL = lightSensorL.light
        lightR = lightSensorR.light
        # uValue = ultra.value
        
        rSpeed = 70-70*(avgR-lightR)/avgR
        lSpeed = 70-70*(avgL-lightL)/avgL

        driveStart(rSpeed,lSpeed)

        time.sleep(0.05)
      except IOError:
        print ("\nError occurred while attempting to read values.")
        stop()
  except KeyboardInterrupt:
    print("\nCtrl+C detected. Exiting...")
    stop()

if __name__ == '__main__':
  main()
  stop()

