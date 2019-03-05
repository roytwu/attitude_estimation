"""
File name:   imu_boxControl.py
Developer:   Roy TWu
Description: Visualizing IMU's rotational motion via a cuboid
    03/01/2019 -- File imported from https://github.com/mattzzw/Arduino-mpu6050
    03/02/2019 -- updated to Python3.7, cuboid image is changed to mimic IMU
"""
import serial
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#* open serial port
#* serial pornt # can be found from "Device Manager" (Windows system)  
#ser = serial.Serial('COM5', 38400, timeout=1)
ser = serial.Serial('COM3', 38400, timeout=1)

ax = ay = az = 0.0
yaw_mode = True

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

    #* holding the IMU board such that IMU coordinate system is same as 
    #* the OpenGL coordinate system

    if yaw_mode:                      #* experimental
        glRotatef(az, 0.0, 0.0, 1.0)  #* Yaw,   rotate around z-axis
    else:
        glRotatef(0.0, 0.0, 0.0, 1.0)
    glRotatef(ay, 0.0, 1.0, 0.0)      #* Pitch, rotate around y-axis
    glRotatef(ax, 1.0, 0.0, 0.0)      #* Roll,  rotate around x-axis
 



    #* decalre the type of primitive
    glBegin(GL_QUADS)	
    
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
         
def read_data():
    global ax, ay, az
    ax = ay = az = 0.0
    line_done = 0
    ser.write(b".") #* request data by sending a dot
    
    #* while not line_done:
    line = ser.readline() 
    angles = line.split(b", ")
    if len(angles) == 3:    
        ax = float(angles[0])
        ay = float(angles[1])
        az = float(angles[2])
        line_done = 1 

#* ----- main function -----
def main():
    global yaw_mode

    video_flags = OPENGL|DOUBLEBUF
    
    #* initialize pyGame and create a window
    pygame.init()
    screen = pygame.display.set_mode((640,480), video_flags)
    pygame.display.set_caption("Press Esc To Quit. Press Z To Toggle Yaw Mode")
    resize(640,480)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()
    
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
       
        draw()
        pygame.display.flip() #* update entire display
        frames = frames+1

    print ("fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks)))
    ser.close()


print(__name__)
if __name__ == '__main__': main()

