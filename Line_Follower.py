# Line_Follower.py

# Created by Colin Adreani on 10/20/2025


# More info and instruction on using this sensor can be found in the basehat folder
# on your Pi's Desktop 

from basehat import LineFinder, IMUSensor
from buildhat import Motor
import time

# set the pin to be used
pinL = 26
pinR = 18

motorL = Motor('A')
motorR = Motor('B')
motorG = Motor('C')

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

def gate(gateBool):
  if gateBool:
    motorG.run_for_degrees(90, 30)
  else:
    motorG.run_for_degrees(-90, 30)

def main():
  try: 
    while True:
      try: 

        # Reading line sensor values
        lineL = lineSensorL.value
        lineR = lineSensorR.value

        # Reading IMU gyro values
        gX, gY, gZ = IMU.getGyro()

        # Reading IMU magnet values
        mX, mY, mZ = IMU.getMag()

        print(f'\n Right Line = {lineL}, Left Line = {lineR}')

        # Sets one side of 
        rSpeed = 5 if lineR else 20
        lSpeed = 5 if lineL else 20

        print(f'rSpeed = {rSpeed}, lSpeed = {lSpeed}, gyroReading = {gZ}')

        driveStart(rSpeed,lSpeed)

        if (mX > 0) or (mY > 0) or (mZ > 0):
          gate(True)
          time.sleep(1)
          gate(False)


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

