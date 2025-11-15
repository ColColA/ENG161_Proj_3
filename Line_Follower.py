# Line_Follower.py

# Created by Colin Adreani on 10/20/2025


# More info and instruction on using this sensor can be found in the basehat folder
# on your Pi's Desktop 

from basehat import LineFinder
from buildhat import Motor
import time

# set the pin to be used
pinL = 22
pinR = 5

motorL = Motor('A')
motorR = Motor('B')

# Initializing the sensor so the function within the class can be used
lineSensorL = LineFinder(pinL)
lineSensorR = LineFinder(pinR)

def drive(rSpeed, lSpeed, time):
  motorR.start(-rSpeed)
  motorL.start(lSpeed)

  time.sleep(time/1000)

  motorR.stop()
  motorL.stop()

def driveStart(rSpeed, lSpeed):
  motorR.start(-rSpeed)
  motorL.start(lSpeed)

def stop():
  motorR.stop()
  motorL.stop()

def main():
  try: 
    while True:
      try: 
        lineL = lineSensorL.value
        lineR = lineSensorR.value

        print(f'\n Right Line = {lineL}, Left Line = {lineR}')

        rSpeed = 70 if lineR else 30
        lSpeed = 70 if lineL else 30

        print(f'rSpeed = {rSpeed}, lSpeed = {lSpeed}')

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

