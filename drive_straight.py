# ------------------------------------------
# Created by Colin Adreani 10/24/25 3:22 pm
# Cruise Control Program for DC 2
# ------------------------------------------

from basehat import Button
from buildhat import Motor
import time

DIAMETER = 3.25
PI = 3.14
CIRCUMFERENCE = DIAMETER * PI

uPin = 5
button_port = 22 # assign button sensor for D22

button = Button(button_port)
motorR = Motor('A')
motorL = Motor('B')

# Before button is pressed, your program will be stuck in this loop
print("Press button on port 22 to run motors")
button.wait_for_press()
print("Starting...")

def drive(rSpeed, lSpeed, setTime):
  motorR.start(rSpeed)
  motorL.start(-lSpeed)

  time.sleep(setTime/1000)

  motorR.stop()
  motorL.stop()

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

# Main logic    
try:
    while True:
        #PUT YOUR LOGIC HERE
        #this infinite loop can be interrupted by ctrl+c a.k.a. keyboardInterrupt 
        maxSpeed = 1.969
        pDrive(maxSpeed)

except IOError as error:
    print(error)
    stop()
except TypeError as error:
    print(error)
    stop()
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
    stop()

