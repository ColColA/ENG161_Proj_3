# Line_Follower.py

# Created by Colin Adreani on 10/20/2025


# More info and instruction on using this sensor can be found in the basehat folder
# on your Pi's Desktop 

from basehat import LineFinder, IMUSensor, Button
from buildhat import Motor
import time, math

# set the pins to be used
pinL = 26
pinR = 18

pinBL = 22
pinBR = 5

# Define object instances of used electronics and define port
motorR = Motor('A')
motorL = Motor('B')
motorG = Motor('D')

IMU = IMUSensor()

buttonL = Button(pinBL)
buttonR = Button(pinBR)

lineSensorL = LineFinder(pinL)
lineSensorR = LineFinder(pinR)

# variable to store the order of turns after startup
turnSequence = []

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
  
  # Updates sensor values within scope of function
  lineL = lineSensorL.value
  lineR = lineSensorR.value

  while True:
    # Updates sensor values within scope of function
    lineL = lineSensorL.value
    lineR = lineSensorR.value

    if lineL and lineR:
      lSpeed = 20
      rSpeed = 20
    else:
      lSpeed = 20 if lineL else 0
      rSpeed = 20 if lineR else 0

    driveStart(rSpeed, lSpeed)

  while lineL == lineR:
    
    # Updates sensor values within scope of function
    lineL = lineSensorL.value
    lineR = lineSensorR.value

    # Turns to the left
    if dir.upper() == 'L' or dir.upper() == "LEFT":

      # Continuously drives to the left while looking for path
      driveStart(35, 10)
      
    # Turns to the right
    elif dir.upper() == 'R' or dir.upper() == "RIGHT":

      # Continuously drives to the right while looking for path
      driveStart(10, 35)

  # drive(20, 20, 1000)

  # # Repeat until line is found
  # while lineL != 0 or lineR != 0 or not flag:
  #   # Updates sensor values within scope of function
  #   lineL = lineSensorL.value
  #   lineR = lineSensorR.value

  #   print(f'Status: LineL: {lineL}, LineR: {lineR}, Flag: {flag}')

  #   # Turns to the left
  #   if dir.upper() == 'L' or dir.upper() == "LEFT":

  #     # Continuously drives to the left while looking for path
  #     driveStart(10, -10)
      
  #   # Turns to the right
  #   elif dir.upper() == 'R' or dir.upper() == "RIGHT":

  #     # Continuously drives to the right while looking for path
  #     driveStart(-10, 10)

  #   # Flips the flag if it leaves the line
  #   if lineL != lineR and flag == False:
  #     flag = True
  turnSequence.pop(0)

# Opens and closes gate
def gate(gateBool):
  if gateBool:
    motorG.run_for_degrees(85, 30)
  else:
    motorG.run_for_degrees(-85, 30)


# Main Loop for running code
def main():
  # Sets up callback functions to update turnSequence when buttons are pressed
  buttonL.when_released = lambda: turnSequence.append("L")
  buttonR.when_released = lambda: turnSequence.append("R")

  isStartup = True
  speedFlag = False
  try: 
    while True:
      try: 
        
        while isStartup:
          stop()
            
          # Reading button sensor values
          bValueL = buttonL.value
          bValueR = buttonR.value

          print(f'\nTurn Sequence: {turnSequence}')
          
          # Checks if both are down, and if so it continues
          if bValueL and bValueR:
            time.sleep(1)
            isStartup = False
            turnSequence.pop()
            turnSequence.pop()
          
          time.sleep(0.2)

        # Reading line sensor values
        lineL = lineSensorL.value
        lineR = lineSensorR.value

        # Reading IMU magnet values
        mX, mY, mZ = IMU.getMag()

        print(f'\n Right Line = {lineR}, Left Line = {lineL}')

        # Detects junction and turns right
        if lineL and lineR:
          turnTillLine(turnSequence[0])

        # Detects devation to the right and corrects
        elif lineL and not lineR:
            motorR.start(20)
            motorL.stop()
        
        # Detects devation to the right and corrects
        elif lineR and not lineL:
            motorR.stop()
            motorL.start(-20)
        
        # Runs motors forward when driving
        else:
            rSpeed = 20
            lSpeed = 20
            driveStart(rSpeed,lSpeed)

            # if (motorR.get_speed()+motorR.get_speed())/2 == (rSpeed+lSpeed)/2 and speedFlag == False:
            #   speedFlag = True

            # if (motorR.get_speed()+motorR.get_speed())/2 < 5 and speedFlag:
            #   drive(-10, -10, 4000)
            #   drive(50, 50, 4000)
            #   speedFlag = False
            # else:
            #   driveStart(rSpeed,lSpeed)

        # Prints status
        print(f'rSpeed = {rSpeed}, lSpeed = {lSpeed}, magReading = {mZ}')

        # # Detects if magnetic goal marker is beneath robot and deploys payload
        # if math.fabs(mZ) > 50:
        #   time.sleep(1)
        #   gate(True)
        #   time.sleep(1)
        #   gate(False)


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