# ------------------------------------------
# Created by Colin Adreani 10/24/25 3:22 pm
# Cruise Control Program for DC 2
# ------------------------------------------

from buildhat import Motor
from basehat import IMUSensor
import time, math

DIAMETER = 3.25
PI = 3.14
CIRCUMFERENCE = DIAMETER * PI

motorL = Motor('A')
motorR = Motor('B')
motorG = Motor('D')

# Initializing the IMU so the example can utilize the sensor
IMU = IMUSensor()

def drive(lSpeed, rSpeed, setTime):
  driveStart(lSpeed, rSpeed)

  time.sleep(setTime/1000)

  motorR.stop()
  motorL.stop()

def gate(gateBool):
  if gateBool:
    motorG.run_for_degrees(85, 10)
  else:
    motorG.run_for_degrees(-85, 10)

def driveStart(lSpeed, rSpeed):
  motorR.start(rSpeed)
  motorL.start(-lSpeed)

def stop():
  motorR.stop()
  motorL.stop()

def pDrive(maxSpeed):
    kp = 1
    kc = 3

    oldPosR = motorR.get_position()
    oldPosL = motorL.get_position()

    time.sleep(.01)

    newPosR = motorR.get_position()
    newPosL = motorL.get_position()

    curSpeedR = 100*CIRCUMFERENCE*(newPosR - oldPosR)/360
    curSpeedL = 100*CIRCUMFERENCE*(newPosL - oldPosL)/360
    print(f'\nright speed = {curSpeedR}, left speed = {curSpeedL}')
    
    rSpeed = 50 + (maxSpeed - curSpeedR)*kp
    lSpeed = 50 + (maxSpeed - curSpeedL)*kp

    driveStart(rSpeed, lSpeed)

def gyroDrive(speed, gZ):
  kp = 1

  rSpeed = speed + kp*(gZ-1.3)
  lSpeed = speed - kp*(gZ-1.3)
  
  if rSpeed > 100 or rSpeed < -100: rSpeed = speed
  if lSpeed > 100 or rSpeed < -100: lSpeed = speed

  driveStart(rSpeed, lSpeed)

# Main logic    
try:
  speed = 20
  magFlag = False
  turnSequence = [[],[True, True]]
  while True:
    #PUT YOUR LOGIC HERE
    #this infinite loop can be interrupted by ctrl+c a.k.a. keyboardInterrupt
    
    mX, mY, mZ = IMU.getMag() 

    driveStart(speed, speed)
    
    print(math.fabs(mZ))

    # Detects if magnetic goal marker is beneath robot and deploys payload
    if math.fabs(mZ) > 500 and magFlag == False:
      magFlag = True
      if turnSequence[1][0]:
        gate(True)
        speed = 100
      turnSequence[1].pop(0)
    elif math.fabs(mZ) < 150 and magFlag == True: 
      magFlag = False
      speed = 20

except IOError as error:
  print(error)
  stop()
except TypeError as error:
  print(error)
  stop()
except KeyboardInterrupt:
  print("You pressed ctrl+C...")
  stop()