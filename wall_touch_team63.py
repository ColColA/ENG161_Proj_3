#wall_stop.py

# Declaring what libraries to include
from basehat import UltrasonicSensor, Button
from buildhat import Motor
import time

# declares a function "main" to run at runtime
def main():
#   Defines a variable called "pin" to use later
    uPin = 5
    bPin = 22
    
    buttonCount = 0
    flag = False
    
#   updates user on status
    print("Initiating BuildHAT and motors")
    print("this may take a while (~10 seconds)")
    
#   creates variables to hold the left and right motor objects at their respective ports
    motorL = Motor('A')
    motorR = Motor('B')

#   creates variables to hold the sensor object at its respective pin
    ultra = UltrasonicSensor(uPin)
    button = Button(bPin)
    buttonValue = button.value

#   runs code to catch errors and stops motors if it fails
    try:
#       infinite loop for the body of the code
        while True:
#           runs code to catch errors and stops motors if it fails
            try:
#               reads distance value from sensor
                buttonValue = button.value
                value = ultra.getDist
                
#               flag system to make the button presses happen incrementally not just spamming it
                if flag == False and buttonValue == 1:
                    buttonCount += 1
                    flag = True
                elif flag == True and buttonValue == 0:
                    flag = False
                    
#               skips the movement code when the button hasn't been pressed twice
                if buttonCount < 2:
                    continue

# 				Updates user on current state of motors (absolute position)
                print(f"Sensor: {value} Motor A: {motorL.get_position()}  B: {motorR.get_position()} ")
#               Check if the distance is reading something and if it is less than 15 
                if(value != None and value < 13):
#                   If so, it stops the motors to make you stop before the wall
                    print("Stopped")
                    motorL.stop()
                    motorR.stop()
                    while (value < 18):
                        value = ultra.getDist
                        
#                       moves backwards
                        motorR.start(-30)
                        motorL.start(30)
                        
                        time.sleep(0.05)
                        
                    motorL.stop()
                    motorR.stop()
                    
#                   Turns in place
                    motorR.start(-30)
                    motorL.start(-30)
                    
                    time.sleep(3)
                    
                    motorL.stop()
                    motorR.stop()
                    
#               Stops the motors on alternating button presses
                elif buttonCount % 2 == 1:
                    motorR.stop()
                    motorL.stop()
                else:
#                   Runs the motors forward
                    motorR.start(30)
                    motorL.start(-30)
                time.sleep(.01)

            except IOError:
#               if theres an error in the reading of the values, stop the motor
                print ("\nError occurred while attempting to read values.")
                motorL.stop()
                motorR.stop()
                break
# 	if the user tells it to stop, stop the motors first
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting...")
        motorL.stop()
        motorR.stop()

# check if this is the main program
if __name__ == '__main__':
#   run main function
    main()
#   make sure motors stop when program is over
    motorL = Motor('A')
    motorR = Motor('B')
    motorL.stop()
    motorR.stop()