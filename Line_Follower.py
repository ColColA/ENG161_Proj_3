# Line_Follower.py

# Created by Colin Adreani on 10/20/2025


# More info and instruction on using this sensor can be found in the basehat folder
# on your Pi's Desktop 

from buildhat import Motor, ColorSensor
import time

motorL = Motor('A')
motorR = Motor('B')
colorSensor = ColorSensor('C')


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
  curTime = time.perf_counter()
  # # set the pin to be used
  # pinL = 0
  # pinR = 0

  # # Initializing the sensor so the function within the class can be used
  # lightSensorL = LightSensor(pinL)
  # lightSensorR = LightSensor(pinR)

  # lightL = lightSensorL.light
  # lightR = lightSensorR.light

  # avgL = 0;
  # avgR = 0;

  # for i in range(0,100):
  #   lightL = lightSensorL.light
  #   lightR = lightSensorR.light

  #   avgL += lightL
  #   avgR += lightR

  #   time.sleep(0.01)
  
  # avgL = avgL/100
  # avgR = avgR/100

  try: 
    while True:
      try: 
        # lightL = lightSensorL.light
        # lightR = lightSensorR.light
        # print(f'\navgL = {avgL}, curL = {lightL} ---- avgR = {avgR}, curR = {lightR}')

        # # update and read the values of the lineFinder
        # lightL = lightSensorL.light
        # lightR = lightSensorR.light
        # # uValue = ultra.value
        
        # rSpeed = 30-40*(avgR-lightR)/avgR
        # lSpeed = 30-40*(avgL-lightL)/avgL
        color = colorSensor.get_color_rgbi
        while color[3] < 130:
          color = colorSensor.get_color_rgbi

          driveStart(50,50)

          time.sleep(0.05)
          curTime = time.perf_counter()
        if (time.perf_counter() - curTime < 1000):
          driveStart(50,-50)
        elif (time.perf_counter() - curTime < 3000):
          driveStart(-50,50)
      except IOError:
        print ("\nError occurred while attempting to read values.")
        stop()
  except KeyboardInterrupt:
    print("\nCtrl+C detected. Exiting...")
    stop()

if __name__ == '__main__':
  main()
  stop()

