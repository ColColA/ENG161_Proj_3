# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 01:05:44 2025

@author: gatro
"""

import math
import time

#this program does not yet account for broken lines

def goStraight ():
    print ('Run both motor speed at speed x rpm')
    
def turnRight():
    print('Run right motor at x rpm forwards and run the left motor at x rpm backwards')
        
def turnLeft():
    print('Run left motor at x rpm forwards and run the right motor at x rpm backwards')
    

    #this program takes the direction that the robot is intitially facing as the direction of the positive x axis

wheelRadius = 1.0 #replace with actual value
r = wheelRadius
currentPosition = [0,0] 
xRpm = 1.0  #replace with actual value
angle = 0.0  #replace with actual value
centerToWheel = 1.0  #the distance from the center of rotation of robot to the center of wheel. SHould be half of the distance between the center of the back wheel to the center of the front wheel. Replace with actual value



while (True):
    
    sensorInputRight = bool(input('Input the snesor input for sensor 1:'))
    sensorInputLeft = bool(input('Input the snesor input for sensor 2:'))
    time1 = time.time() #start time
    
    
    #For going straight, we add the distance travelled in both the x and y direction to currentPosition
    if(sensorInputRight and sensorInputLeft): #both sensors are detecting line
        goStraight()
        time2 = time.time() 
        deltaT = time2 - time1
        print(f'deltaT: {deltaT}')
        currentPosition[0] = currentPosition[0] + (2*math.pi*r*xRpm*deltaT)*math.cos(angle)
        currentPosition[1] = currentPosition[1] + (2*math.pi*r*xRpm*deltaT)*math.sin(angle)
        
    
    #When we detect that we need to turn right, we adjust the angle depending on how long we turn for
    elif(sensorInputRight and not sensorInputLeft):
        turnRight()
        time2 = time.time()
        deltaT = time2 - time1
        print(f'deltaT: {deltaT}')
        angle = -2*(math.pi)*((2*math.pi*r*xRpm*deltaT)/2*math.pi*centerToWheel)   #if the robot rotates about its center, then the wheels should travel in a circle around this center. Assuming the wheels do not slip, the distance travelled by the wheels on this circle should be the 2(pi)r*xrpm*time. Knowing this, we can calculate the angle of this arc. 
        
        
    elif(not sensorInputRight and sensorInputLeft):
        turnLeft()
        time2 = time.time()
        deltaT = time2 - time1
        print(f'deltaT: {deltaT}')
        angle = 2*(math.pi)*((2*math.pi*r*xRpm*deltaT)/2*math.pi*centerToWheel)
        
    print (currentPosition)
    
    

    



    

    
