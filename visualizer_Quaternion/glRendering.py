"""
Developer:   Roy TWu
File Name:   glRendering.py
Description: OpenGL rendering
"""
import numpy
import pygame
from pygame.locals import *
from OpenGL.GL     import *
from OpenGL.GLU    import *


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


#* ----- ----- ----- ----- ----- ----- -----
def draw(angleAxis):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
    
    glLoadIdentity()
    glTranslatef(0,0.0,-7.0)

#    osd_text = "pitch: " + str("{0:.2f}".format(ay)) \
#               + ", roll: " + str("{0:.2f}".format(ax))
#    osd_line = osd_text + ", yaw: " + str("{0:.2f}".format(az))
#    drawText((-2,-2, 2), osd_line)  #* draw on-screen text

    
    #* rotate cuboid
    theta = angleAxis[0]
    a1 = angleAxis[1]
    a2 = angleAxis[2]
    a3 = angleAxis[3]
    glRotatef(theta, a1, a2, a3)
    
    #* draw cuboid
    cuboid()
#* ----- ----- ----- ----- ----- ----- -----      



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


def cuboid():
    #*----- cuboid 1 -----
    glBegin(GL_LINES)
    for edge in tup_edges:
        for node in edge:
            glVertex3fv(tup_vertices[node])
    glEnd()
    
    
    #*----- cuboid 2 -----
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

