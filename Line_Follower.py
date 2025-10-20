# Line_Follower.py

# Created by Colin Adreani on 10/20/2025


# More info and instruction on using this sensor can be found in the basehat folder
# on your Pi's Desktop 

from basehat import LineFinder, UltrasonicSensor
from buildhat import Motor
import time

uPin = 5

motorL = Motor('A')
motorR = Motor('B')

ultra = UltrasonicSensor(uPin)

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
  pin = 5

  # Initializing the sensor so the function within the class can be used
  lineFinder = LineFinder(pin)

  try: 
    while True:
      try: 
        while curValue == 0:
          # update and read the values of the lineFinder
          lineValue = lineFinder.value
          uValue = ultra.value

          if (uValue != None and value < 13):
            stop()
            while value < 18:
              driveStart(-50, -50)
            stop()
            drive(-50, 50, 2500)
          else: 
            driveStart(50,50)

          # print values
          print("LineFinder value: {}".format(lineValue))
          print("Ultrasonic value: {}".format(uValue))

          time.sleep(0.1)
      drive(50, 0, 750)
      lineValue = lineFinder.value
      if lineValue == 1:
        continue
      drive(0, 50, 1500)
      lineValue = lineFinder.value
      if lineValue == 1:
        continue
      except IOError:
        print ("\nError occurred while attempting to read values.")
        stop()
        break

  except KeyboardInterrupt:
    print("\nCtrl+C detected. Exiting...")
    stop()

if __name__ == '__main__':
  main()
  stop()

