"""
Created on Sun Dec  7 11:56:40 2025

@author: gatro
"""


import time
import math
from buildhat import Motor
#takes target velocity and converts to inches/sec
targetV = 0.393701*(float(input ("Input the desired speed (cm/sec) here: " )))
    
distance = 0
diameter = 2.75
pi = math.pi
targetRPS = targetV/(diameter*pi)

motorL = Motor('A')
motorR = Motor('B')


#converts units of RPS to motor speed units
def unitConverter (value):
    final = (value - 0.095)/0.02375
    return(final)

try:
    while (distance < 100.9): 
       
        t0 = time.perf_counter()    
        
        #tells motors to go at desired speed (converted to motor speed units) I added 1.0 to the left motor because the robot wasnt driving straight when motors were going same speed
        motorR.start(unitConverter(targetRPS))
        motorL.start(-unitConverter(targetRPS))
        
        t1 = time.perf_counter()
        tDiff = t1 - t0
        
        if (tDiff > 0.01):
            tDiff = 0
            
        #multiplied by 8.4 because the values were off by a factor of 8.43 (8.43 is a bit high, but thats good because it makes the robot stop before the finish). This is probably due to tDiff not encapsulating all time spent
        distance += 8.4*diameter*pi*targetV*tDiff
        
        print(distance)

except KeyboardInterrupt:
    print("\nCtrl+C detected. Exiting...")
    motorR.stop()
    motorL.stop()
        
motorR.stop()
motorL.stop()
