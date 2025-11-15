# ------------------------------------------
# Created by Colin Adreani 10/24/25 3:22 pm
# Cruise Control Program for DC 2
# ------------------------------------------

from buildhat import Motor, IMUSensor
import time

DIAMETER = 3.25
PI = 3.14
CIRCUMFERENCE = DIAMETER * PI

motorR = Motor('A')
motorL = Motor('B')
motorG = Motor('C')

# Initializing the IMU so the example can utilize the sensor
IMU = IMUSensor()

def drive(rSpeed, lSpeed, setTime):
  motorR.start(rSpeed)
  motorL.start(-lSpeed)

  time.sleep(setTime/1000)

  motorR.stop()
  motorL.stop()

def gate(gateBool):
  if gateBool:
    motorG.run_for_degrees(90, 50)
  else:
    motorG.run_for_degrees(-90, 50)

def driveStart(rSpeed, lSpeed):
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

def gyroDrive(speed, heading, gZ):
  kp = 1

  rSpeed = speed + kp*(heading - gZ)
  lSpeed = speed + kp*(heading - gZ)

  driveStart(rSpeed, lSpeed)

# Main logic    
try:
    while True:
        #PUT YOUR LOGIC HERE
        #this infinite loop can be interrupted by ctrl+c a.k.a. keyboardInterrupt 
        # driveStart(50, 50)
        x, y, z = IMU.getGyro()

        gyroDrive(20, 0, z)

except IOError as error:
    print(error)
    stop()
except TypeError as error:
    print(error)
    stop()
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
    stop()