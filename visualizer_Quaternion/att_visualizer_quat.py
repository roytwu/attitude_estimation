"""
File name:   imu_boxControl.py
Developer:   Roy TWu
Description: Visualizing IMU's rotational motion via a cuboid
    03/01/2019 -- File imported from https://github.com/mattzzw/Arduino-mpu6050
    03/02/2019 -- updated to Python3.7, cuboid image is changed to mimic IMU
    03/14/2019 -- output gyro data from Arduino firmware
"""
import math
import serial
import pygame
import quaternion as Quat
from math          import cos
from math          import sin
from math          import sqrt
from pygame.locals import *
from OpenGL.GL     import *
from OpenGL.GLU    import *

#* open serial port
#* serial pornt # can be found from "Device Manager" (Windows system)  
ser = serial.Serial('COM5', 38400, timeout=1)
#ser = serial.Serial('COM3', 38400, timeout=1)

theta = a1 = a2 = a3 = 0.0
ax = ay = az = 0.0
yaw_mode = True
dt = 1.0/30.0;

def resize(width, height):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def drawText(position, textString):     
    font = pygame.font.SysFont ("Courier", 18, True)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, 
                 GL_UNSIGNED_BYTE, textData)


tup_vertices= (
    ( 1.0, -1.5, -0.2),  #* lower right back
    ( 1.0,  1.5, -0.2),  #* upper right back
    (-1.0,  1.5, -0.2),  #* upper left back
    (-1.0, -1.5, -0.2),  #* lower left back
    ( 1.0, -1.5,  0.5),  #* lower right front
    ( 1.0,  1.5,  0.5),  #* upper right fromt
    (-1.0,  1.5,  0.5),  #* upper left front 
    (-1.0, -1.5,  0.5)   #* lower left front
)

tup_edges = (    
    (0,1), (0,3), (0,4),
    (2,1), (2,3), (2,6),
    (7,3), (7,4), (7,6),
    (5,1), (5,4), (5,6)
)


#* ----- ----- read data ----- -----   
def read_data():
    global ax, ay, az
    global gyrX, gyrY, gyrZ 
    ax = ay = az = 0.0
    gyrX = gyrY = gyrZ = 0.0
    line_done = 0
    ser.write(b".") #* request data by sending a dot
    
    #* while not line_done:
    line = ser.readline() 
    angles = line.split(b", ")
    if len(angles) == 6:    
        ax = float(angles[0]) #*Euler angle x
        ay = float(angles[1]) #*Euler angle y
        az = float(angles[2]) #*Euler angle z
        gyrX = math.radians(float(angles[3])) 
        gyrY = math.radians(float(angles[4])) 
        gyrZ = math.radians(float(angles[5])) 
        line_done = 1 
    
    print('gyro data output...', gyrX, gyrZ, gyrZ)

#* ----- ----- integration ----- -----  
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
    
    #* Unit Quaternion to angle-axis
    if q0*q0 == 1.0:
        print('Null rotation\n')
        theta = 0
        a1    = 1 
        a2    = 0 
        a3    = 0
    else:
        theta = math.degrees(2*math.acos(q0))
        foo   = math.sqrt(1-q0*q0)
        a1    = q1/foo
        a2    = q2/foo
        a3    = q3/foo  

#* ----- ----- draw ----- -----  
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

    drawText((-2,-2, 2), osd_line)  #* draw on-screen text

    #* math the OpenFL coordinate frame to World frame
#    glRotatef(-90, 1.0, 0.0, 0.0)
    
    #* holding the IMU board such that IMU coordinate system is same as 
    #* the OpenGL coordinate system
    #* z-y-x Euler angle, R = Rz*Ry*Rx
#    glRotatef(ax, 1.0, 0.0, 0.0)      #* Roll,  rotate around x-axis
#    glRotatef(ay, 0.0, 1.0, 0.0)      #* Pitch, rotate around y-axis
#    if yaw_mode:                      
#        glRotatef(az, 0.0, 0.0, 1.0)  #* Yaw,   rotate around z-axis
#    else:
#        glRotatef(0.0, 0.0, 0.0, 1.0)
    
    #* Unit Quaternion to angle-axis
    glRotatef(theta, a1, a2, a3)
    
    glBegin(GL_LINES)
    for edge in tup_edges:
        for node in edge:
            glVertex3fv(tup_vertices[node])
    glEnd()
    
    glBegin(GL_QUADS) #* decalre the type of primitive
    #* top
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f( 1.0, 1.5, -0.2)   
    glVertex3f(-1.0, 1.5, -0.2)		
    glVertex3f(-1.0, 1.5,  0.2)		
    glVertex3f( 1.0, 1.5,  0.2)		

    #* buttom 
    glColor3f(0.0, 0.0, 1.0)	
    glVertex3f( 1.0, -1.5, -0.2)
    glVertex3f(-1.0, -1.5, -0.2)		
    glVertex3f(-1.0, -1.5,  0.2)		
    glVertex3f( 1.0, -1.5,  0.2)		

    #* front
    glColor3f(1.0, 0.0, 0.0)		
    glVertex3f( 1.0,  1.5, 0.2)
    glVertex3f(-1.0,  1.5, 0.2)		
    glVertex3f(-1.0, -1.5, 0.2)		
    glVertex3f( 1.0, -1.5, 0.2)		

    #* back
    glColor3f(0.0, 1.0, 0.0)	
    glVertex3f( 1.0,  1.5, -0.2)
    glVertex3f(-1.0,  1.5, -0.2)		
    glVertex3f(-1.0, -1.5, -0.2)		
    glVertex3f( 1.0, -1.5, -0.2)	

    #* left
    glColor3f(0.0, 0.0, 1.0)	
    glVertex3f(-1.0,  1.5,  0.2)
    glVertex3f(-1.0,  1.5, -0.2)		
    glVertex3f(-1.0, -1.5, -0.2)		
    glVertex3f(-1.0, -1.5,  0.2)		

    #* right
    glColor3f(0.0, 0.0, 1.0)	
    glVertex3f(1.0,  1.5,  0.2)
    glVertex3f(1.0,  1.5, -0.2)		
    glVertex3f(1.0, -1.5, -0.2)		
    glVertex3f(1.0, -1.5,  0.2)		
    glEnd()	
      


#* ----- main function -----
def main():
    global yaw_mode
    global initQ

    video_flags = OPENGL|DOUBLEBUF
    
    #* initialize pyGame and create a window
    pygame.init()
    screen = pygame.display.set_mode((640,480), video_flags)
    pygame.display.set_caption("Press Esc To Quit. Press Z To Toggle Yaw Mode")
    resize(640,480)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()
    
    initQ = [1, 0, 0, 0]
    
    while 1:
        event = pygame.event.poll()
        #* Fix: pyGame window does not close when close button is pressed
        #* 2 way to close the window: click the x button on top of the window 
        #*                            or hit Esc key
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
        
        pygame.display.flip() #* update entire display
        frames = frames+1

    print ("fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks)))
    ser.close()


print(__name__)
if __name__ == '__main__': main()

