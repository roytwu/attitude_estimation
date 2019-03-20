"""
File name:   _attVisualizer_quat.py
Developer:   Roy TWu
Description: Quaternion-based attitude estimation
             Visualizing IMU's rotational motion via a cuboid
History:              
    03/01/2019 -- File imported from https://github.com/mattzzw/Arduino-mpu6050
    03/02/2019 -- updated to Python3.7, cuboid shape is changed
    03/14/2019 -- * updating Arduino file to output gyro data 
                  * moving the integration part from .ino to python script
                  * Eular-angle version is commentted out
                  * moving part of OpenGL to separate script
    03/20/2019 --               
                  
"""
import math
import numpy as np  
import serial
import pygame
from numpy.linalg  import norm
from math          import sin, cos, sqrt
from pygame.locals import *
from OpenGL.GL     import *
from OpenGL.GLU    import *

import quaternion  as Quat
import glRendering as GL

#* open serial port
#* serial pornt # can be found from "Device Manager" (Windows)  
ser = serial.Serial('COM5', 38400, timeout=1)
#ser = serial.Serial('COM3', 38400, timeout=1)

dt = 1.0/30.0;  
#* ----- ----- read data ----- -----   
#* raw gryo data from MPU6050 is in degrees, convert to radians here
def read_data():
    global acc, gyr #*numpy array
    accX = accY = accZ = 0
    gyrX = gyrY = gyrZ = 0
    line_done = 0
    ser.write(b".") #* request data by sending a dot
    
    #* while not line_done:
    line = ser.readline() 
    angles = line.split(b", ")
    if len(angles) == 6:    
        accX = float(angles[0])  #* accelerometer measurement X
        accY = float(angles[1])  #* accelerometer measurement Y
        accZ = float(angles[2])  #* accelerometer measurement Z
        gyrX = math.radians(float(angles[3])) #* convert from degrees to radians
        gyrY = math.radians(float(angles[4])) 
        gyrZ = math.radians(float(angles[5])) 
        line_done = 1 
            
    #print('gyro data output...', gyrX, gyrZ, gyrZ)
    acc = np.array([accX, accY, accZ])
    gyr = np.array([gyrX, gyrY, gyrZ])

#* ----- ----- integrate gyro output ----- -----  
def gyro_integration():
    global dt
    global gyr
    global initQ
    
    norm_w = norm(gyr)
    if norm_w == 0 :
        return
    
    gyrX = gyr[0]
    gyrY = gyr[1]
    gyrZ = gyr[2]
    
    dq0 = cos(dt*norm_w/2)
    dq1 = (gyrX/norm_w)*sin(dt*norm_w/2)
    dq2 = (gyrY/norm_w)*sin(dt*norm_w/2)
    dq3 = (gyrZ/norm_w)*sin(dt*norm_w/2)    
    dQ = np.array([dq0, dq1, dq2, dq3])

    initQ = Quat.multiplication(initQ, dQ)
    #* normalize again to avoid numerical integrtion issues 
    if initQ[0] >= 1:
        initQ[0] = 1
    elif initQ[0] <= -1:
        initQ[0] = -1
    

#* ----- ----- tilt correction ----- -----  
def tilt_correction():
    global initQ
    global acc
    resultQ = np.array([1.0, 0.0, 0.0, 0.0])
    g = np.array([ 0.0, 0.0, -1.0])  #* normalized gravity vector
    
    norm_a = norm(acc)
    if norm_a == 0 :
        resultQ = np.array([1.0, 0.0, 0.0, 0.0])
        return resultQ
    
    #* quaternion-ized vector, 4x1
    accQ = np.append(0, acc/norm_a) 
     
    #* transfrom accQ to global frame
    dummy = Quat.multiplication(initQ, accQ)
    G_accQ = Quat.multiplication(dummy, Quat.inverse(initQ))
    G_acc = G_accQ[1:] #* convert back to 3x1 vector 
    G_acc = G_acc/norm(G_acc)
    print("norm of G_acc is ... ", norm(G_acc))
    
    
    #* finding out angle & axis regarding tilt correction 
    n = np.cross(G_acc, g) 
    phi = math.acos(-G_acc[2])
    #print("phi is ... ", phi)
    
    #* complementary filter parameter
    alpha = 0.9
    phi = (1.0-alpha)*phi
    
    aa = np.append(phi, n)
    resultQ = Quat.RodriguesToQuat(aa)
    
    
    print("resultQ is ... ", resultQ)
    return resultQ
    

#* ----- main function -----
def main():
    global initQ

    #* initialize pyGame and create a window
    pygame.init()
    video_flags = OPENGL|DOUBLEBUF
    screen = pygame.display.set_mode((640,480), video_flags)
    pygame.display.set_caption("Press Esc To Quit")
    GL.resize(640,480)
    GL.init()
    frames = 0
    ticks = pygame.time.get_ticks()
    
    initQ = np.array([1.0, 0.0, 0.0, 0.0])
    
    while 1:
        event = pygame.event.poll()
        #* click the x button on top of the window or hit Esc key to quit 
        if event.type == pygame.QUIT or \
        (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()  #* quit pygame properly
            break       
            
        #* reading data from Arduino
        read_data()
       
        #* implementing algorithm
        gyro_integration()
        #print("initQ is ...", initQ)
        
        
        #* complementary filter
        tcQ = tilt_correction()
        filteredQ = Quat.multiplication(tcQ, initQ)
        
        #* convert quaternion to angl-axis representation
        angleAxis = Quat.quatToRodrigues(filteredQ)
        
        #* pygam & OpenGL rendering
        #* Note: holding the IMU board such that IMU coordinate system is   
        #*       same as the OpenGL coordinate system  
        GL.draw(angleAxis)
        
        #* update entire display
        pygame.display.flip() 
        frames = frames + 1

    print ("fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks)))
    ser.close()


print(__name__)
if __name__ == '__main__': main()

