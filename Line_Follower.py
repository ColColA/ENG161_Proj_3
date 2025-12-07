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
motorL = Motor('A')
motorR = Motor('B')
motorG = Motor('D')

IMU = IMUSensor()

buttonL = Button(pinBL)
buttonR = Button(pinBR)

lineSensorL = LineFinder(pinL)
lineSensorR = LineFinder(pinR)

# variable to store the order of turns after startup
turnSequence = []

class turnType:
  @staticmethod
  def openStraight():
    print("\n\nGoing Straight\n\n")
    drive(-5, 25, 2000)
  
  @staticmethod
  def openRight():
    print("\n\nGoing Right\n\n")
    drive(20, 0, 2000)

  @staticmethod
  def openLeft():
    print("\n\nGoing Left\n\n")
    drive(0, 20, 2000)

  @staticmethod
  def jointLeft():
    print("\n\nIgnoring Left Branch\n\n")
    drive(25, 5, 2000)

  @staticmethod
  def jointRight():
    print("\n\nIgnoring Right Branch\n\n")
    drive(0, 25, 2000)
  
  @staticmethod
  def bump():
    print("\n\nGoing over Bumb\n\n")
    backWheelUp = False
    frontWheelUp = False
    frontWheelDown = True

    while not backWheelUp:

      # Reading line sensor values
      lineL = lineSensorL.value
      lineR = lineSensorR.value

      # Reading IMU gyro values
      gX, gY, gZ = IMU.getGyro()
      
      gX = math.fabs(gX)

      print(f'{gX}\n')

      if (gX > 50 and not frontWheelUp and frontWheelDown):
        print("front wheels over\n")
        frontWheelUp = True
        frontWheelDown = False
      elif (gX < 50 and frontWheelUp and not frontWheelDown):
        print("front wheels down\n")
        frontWheelDown = True
        time.sleep(0.5)
      elif (gX > 50 and frontWheelUp and frontWheelDown):
        print("back wheels over\n")
        backWheelUp = True
      
      driveStart(50, 50)

      # Detects devation to the right and corrects
      if lineL and not lineR and frontWheelDown:
          motorL.start(20)
      
      # Detects devation to the right and corrects
      elif lineR and not lineL and frontWheelDown:
          motorR.start(-20)
    
# General motor start function, can be continuously updated
def driveStart(lSpeed, rSpeed):
  motorR.start(rSpeed)
  motorL.start(-lSpeed)

# General time-based drive code for hardcoding paths
def drive(lSpeed, rSpeed, wt):
  driveStart(lSpeed, rSpeed)

  time.sleep(wt/1000)

  motorR.stop()
  motorL.stop()

# Stops motors from moving
def stop():
  motorR.stop()
  motorL.stop()

# Opens and closes gate
def gate(gateBool):
  if gateBool:
    motorG.run_for_degrees(85, 30)
  else:
    motorG.run_for_degrees(-85, 30)


# Main Loop for running code
def main():
  sequenceA = [["OS", "JR", "OS", "OR", "OS", "JL", "JL"],[False, True]]
  sequenceB = [["OS", "JR", "OS", "OS", "OR", "JS", "JL"],[False, False, True]]
  sequenceC = [["OS", "JR", "OS", "OS", "OS", "JR", "JS"],[False, False, True]]
  test1 = [["BU", "OL", "JR"],[True, True, True]]
  test3 = [["OS", "JR", "OR", "OR"],[False, True, True]]
  turnSequence = []

  # # Sets up callback functions to update turnSequence when buttons are pressed
  # buttonL.when_released = lambda: turnSequence.append("L")
  # buttonR.when_released = lambda: turnSequence.append("R")

  isStartup = True
  isButtonDown = False
  magFlag = False

  lSpeed = 0
  rSpeed = 0

  speed = 20
  try: 
    while True:
      try: 
        
        while isStartup:
          stop()
          motorG.stop()

          # Reading button sensor values
          bValueL = buttonL.value
          bValueR = buttonR.value

          print("Looking For Sequence, Press a Button\n")

          if bValueL and not bValueR and isButtonDown == False:
            turnSequence = test1
            isButtonDown = True
            isStartup = False
            time.sleep(1)
            print(f'\nTurn Sequence: {turnSequence}')
            break
          elif not bValueL and bValueR and isButtonDown == False:
            turnSequence = test1
            isButtonDown = True
            isStartup = False
            time.sleep(1)
            print(f'\nTurn Sequence: {turnSequence}')
            break
          elif bValueL and bValueR and isButtonDown == False:
            turnSequence = sequenceC
            isButtonDown = True
            isStartup = False
            time.sleep(1)
            print(f'\nTurn Sequence: {turnSequence}')
            break
          else:
            isButtonDown = False 

          time.sleep(0.2)

        # Reading line sensor values
        lineL = lineSensorL.value
        lineR = lineSensorR.value

        # Reading IMU magnet values
        mX, mY, mZ = IMU.getMag()

        # Reading acceleration values
        aX, aY, aZ = IMU.getAccel()
        
        # Reading IMU gyro values
        gX, gY, gZ = IMU.getGyro()

        print(f'\n Right Line = {lineR}, Left Line = {lineL}')

        # Detects junction and turns right
        if lineL and lineR:
          try:
            direction = turnSequence[0][0]

            if direction.upper() == 'OS': turnType.openStraight()

            elif direction.upper() == 'OR':turnType.openRight()
            
            elif direction.upper() == 'OL':turnType.openRight()

            elif direction.upper() == 'JR':turnType.jointRight()

            elif direction.upper() == 'JL':turnType.jointLeft()

            elif direction.upper() == 'BU':turnType.bump()

            turnSequence[0].pop(0)
          except IndexError:
            print ("\nError occurred while attempting to index values.")
            stop()
            break

        # Detects devation to the right and corrects
        elif lineL and not lineR:
            motorR.start(speed)
            motorL.stop()
        
        # Detects devation to the right and corrects
        elif lineR and not lineL:
            motorR.stop()
            motorL.start(-speed)
        
        # Runs motors forward when driving
        else:
            rSpeed = speed
            lSpeed = speed

            if (aZ > -9.8):
              driveStart(80,80)
            else:
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
        print(f'rSpeed = {rSpeed}, lSpeed = {lSpeed}, magReading = {mZ}, aZ = {aZ}, gX = {math.fabs(gX)}')

        # Detects if magnetic goal marker is beneath robot and deploys payload
        if math.fabs(mZ) > 500 and magFlag == False:
          magFlag = True
          if turnSequence[1][0]:
            gate(True)
            speed = 100
          turnSequence[1].pop(0)
        elif math.fabs(mZ) < 500 and magFlag == True: 
          magFlag = False
          speed = 20


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