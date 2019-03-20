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
import numpy
import serial
import pygame
from math          import cos
from math          import sin
from math          import sqrt
from pygame.locals import *
from OpenGL.GL     import *
from OpenGL.GLU    import *

import quaternion  as Quat
import glRendering as GL

#* open serial port
#* serial pornt # can be found from "Device Manager" (Windows)  
ser = serial.Serial('COM5', 38400, timeout=1)
#ser = serial.Serial('COM3', 38400, timeout=1)

theta = a1 = a2 = a3 = 0.0
ax = ay = az = 0.0
yaw_mode = True
dt = 1.0/30.0;  

#* ----- ----- read data ----- -----   
#* raw gryo data from MPU6050 is in degrees, convert to radians here
def read_data():
    global accX, accY, accZ
    global gyrX, gyrY, gyrZ 
    accX = accY = accZ = 0.0
    gyrX = gyrY = gyrZ = 0.0
    line_done = 0
    ser.write(b".") #* request data by sending a dot
    
    #* while not line_done:
    line = ser.readline() 
    angles = line.split(b", ")
    if len(angles) == 6:    
        accX = float(angles[0])  #* accelerometer measurement X
        accY = float(angles[1])  #* accelerometer measurement Y
        accZ = float(angles[2])  #* accelerometer measurement Z
        gyrX = math.radians(float(angles[3])) 
        gyrY = math.radians(float(angles[4])) 
        gyrZ = math.radians(float(angles[5])) 
        line_done = 1 
        
    print('gyro data output...', gyrX, gyrZ, gyrZ)


#* ----- ----- integrate gyro output ----- -----  
def gyro_integration():
    global theta, a1, a2, a3
    global dt
    global initQ
    norm_w = sqrt(math.pow(gyrX,2) + math.pow(gyrY,2) + math.pow(gyrZ,2))
    
    if norm_w == 0 :
        return
    
    print('norm_w is ...', norm_w)
    dq0 = cos(dt*norm_w/2)
    dq1 = (gyrX/norm_w)*sin(dt*norm_w/2)
    dq2 = (gyrY/norm_w)*sin(dt*norm_w/2)
    dq3 = (gyrZ/norm_w)*sin(dt*norm_w/2)    
    dQ = [dq0, dq1, dq2, dq3]

    initQ = Quat.multiplication(initQ, dQ)
    q0 = initQ[0]  
    q1 = initQ[1]
    q2 = initQ[2]
    q3 = initQ[3]
  
    print('\nqq0 is... ', q0, '\n')
    if q0 >= 1:
        q0 = 1
    elif q0 <= -1:
        q0 = -1
    
    #* convert unit Quaternion to angle-axis representation
    if q0*q0 == 1.0:
        print('Null rotation\n')
        theta = 0
        a1    = 1 
        a2    = 0 
        a3    = 0
    else:
        theta = math.degrees(2*math.acos(q0)) #*angle
        foo   = math.sqrt(1-q0*q0)
        a1    = q1/foo   #* axis element 1
        a2    = q2/foo   #* axis element 2
        a3    = q3/foo   #* axis element 3


#* ----- ----- tilt correction ----- -----  
def tilt_correction():
    #* normalized gravity vector
    g = [ 0, 0, -1] 
    
    norm_a = sqrt(math.pow(accX,2) + math.pow(accY,2) + math.pow(accZ,2))
    accQ = [0, accX/norm_a, accY/norm_a, accZ/norm_a] #*quaternion-ized vector
    
    dummy = Quat.multiplication(initQ, accQ)
    G_accQ = Quat.multiplication(dummy, Quat.inverse(accQ))
    G_acc = [G_accQ[1], G_accQ[2], G_accQ[3]]
    
    n = numpy.cross(G_acc, g)
    phi = math.acos(-G_acc[2])
    Qn = [phi, n[0], n[1], n[2]]
    

#* ----- ----- draw ----- -----  
#* holding the IMU board such that IMU coordinate system is same as 
#* the OpenGL coordinate system  
def draw():
    global rquad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
    
    glLoadIdentity()
    glTranslatef(0,0.0,-7.0)

    osd_text = "pitch: " + str("{0:.2f}".format(ay)) \
               + ", roll: " + str("{0:.2f}".format(ax))

    if yaw_mode:
        osd_line = osd_text + ", yaw: " + str("{0:.2f}".format(az))
    else:
        osd_line = osd_text

    GL.drawText((-2,-2, 2), osd_line)  #* draw on-screen text

    
    #* rotate cuboid
    glRotatef(theta, a1, a2, a3)
    
    #* draw cuboid
    GL.cuboid()
      


#* ----- main function -----
def main():
    global yaw_mode
    global initQ

    video_flags = OPENGL|DOUBLEBUF
    
    #* initialize pyGame and create a window
    pygame.init()
    screen = pygame.display.set_mode((640,480), video_flags)
    pygame.display.set_caption("Press Esc To Quit. Press Z To Toggle Yaw Mode")
    GL.resize(640,480)
    GL.init()
    frames = 0
    ticks = pygame.time.get_ticks()
    
    initQ = [1, 0, 0, 0]
    
    while 1:
        event = pygame.event.poll()
        #* click the x button on top of the window or hit Esc key to quit 
        if event.type == pygame.QUIT or \
        (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()  #* quit pygame properly
            break       
        if event.type == KEYDOWN and event.key == K_z:
            yaw_mode = not yaw_mode
            ser.write(b"z")
            
        #* reading data from Arduino
        read_data()
       
        #* implementing algorithm
        gyro_integration()
        
        
        #* pygam and OpenGL
        draw()
        
        #* update entire display
        pygame.display.flip() 
        frames = frames+1

    print ("fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks)))
    ser.close()


print(__name__)
if __name__ == '__main__': main()

