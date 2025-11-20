# Line_Follower.py

# Created by Colin Adreani on 10/20/2025


# More info and instruction on using this sensor can be found in the basehat folder
# on your Pi's Desktop 

from basehat import LineFinder, IMUSensor, Button
from buildhat import Motor
import time

# set the pins to be used
pinL = 26
pinR = 18

pinBL = 5
pinBR = 22

# Define object instances of used electronics and define port
motorR = Motor('A')
motorL = Motor('B')
motorG = Motor('D')

IMU = IMUSensor()

buttonL = Button(pinBL)
buttonR = Button(pinBR)

lineSensorL = LineFinder(pinL)
lineSensorR = LineFinder(pinR)

# General time-based drive code for hardcoding paths
def drive(rSpeed, lSpeed, time):
  motorR.start(rSpeed)
  motorL.start(-lSpeed)

  time.sleep(time/1000)

  motorR.stop()
  motorL.stop()

# General motor start function, can be continuously updated
def driveStart(rSpeed, lSpeed):
  motorR.start(rSpeed)
  motorL.start(-lSpeed)

# Stops motors from moving
def stop():
  motorR.stop()
  motorL.stop()

# Turn until it sees a line function for use in pathfinding
def turnTillLine(dir):
  # Keeps track of what has been found
  flag = False

  # Repeat until line is found
  while True:
    # Updates sensor values within scope of function
    lineL = lineSensorL.value
    lineR = lineSensorR.value

    # Turns to the left
    if dir.upper() == 'L' or dir.upper() == "LEFT":

      # Continuously drives to the left while looking for path
      driveStart(-10, 10)

      # Flips the flag if it leaves the line
      if lineL != lineR and flag == False:
        flag == True

      # Ends once it is locked onto the line
      if lineL == 0 and lineR == 0 and flag == True:
        break

    # Turns to the Right
    if dir.upper() == 'R' or dir.upper() == "RIGHT":
      
      # Continuously drives to the right while looking for path
      driveStart(10, -10)

      # Flips the flag if it leaves the line
      if lineL != lineR and flag == False:
        flag == True

      # Ends once it is locked onto the line
      if lineL == 0 and lineR == 0 and flag == True:
        break

# Opens and closes gate
def gate(gateBool):
  if gateBool:
    motorG.run_for_degrees(90, 30)
  else:
    motorG.run_for_degrees(-90, 30)

# Main Loop for running code
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

        print(f'\n Right Line = {lineR}, Left Line = {lineL}')

        # Detects junction and turns right
        if lineL == 1 and lineR == 1:
          turnTillLine("R")

        # Detects devation to the right and corrects
        elif lineL and not lineR:
            motorR.start(35)
            motorL.stop()
            
        # Detects devation to the right and corrects
        elif lineR and not lineL:
            motorR.stop()
            motorL.start(-35)
        
        # Runs motors forward when driving
        else:
            rSpeed = 10
            lSpeed = 10
            driveStart(rSpeed,lSpeed)

        # Prints status
        print(f'rSpeed = {rSpeed}, lSpeed = {lSpeed}, gyroReading = {gZ}')

        # Detects if magnetic goal marker is beneath robot and deploys payload
        if math.fabs(mZ) > 50:
          time.sleep(1)
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

# Runs Main at startup and stops motors when over
if __name__ == '__main__':
  main()
  stop()

