"""
Developer:   Roy TWu
File Name:   quaternion.py
Description: Custom module about quaternion multiplication
"""

import math

#* multiplication of 2 quaternions
def multiplication(p, q):
    p0 = p[0]
    p1 = p[1]
    p2 = p[2]
    p3 = p[3]
    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3]    
    
    r0 = p0 * q0 - (p1 * q1 + p2 * q2 + p3 * q3)
    r1 = p0 * q1 + q0*p1 + (p2 * q3 - p3 * q2)
    r2 = p0 * q2 + q0*p2 + (p3 * q1 - p1 * q3)  
    r3 = p0 * q3 + q0*p3 + (p1 * q2 - p2 * q1) 
    
    r = [r0, r1, r2, r3]
    return r


#* find out quaternion inverse
def quat_inverse(q):
    #* quaternion conjugate 
    q0 = q[0]
    q1 = -q[1]
    q2 = -q[2]
    q3 = -q[3]    
    
    normQ = math.sqrt(
        math.pow(q0,2) + math.pow(q1,2) + math.pow(q2,2) +math.pow(q3,2)
        )
    
    #* normalized conjugate leads to quaternion inverse
    invq0 = q0/normQ
    invq1 = q1/normQ
    invq2 = q2/normQ
    invq3 = q3/normQ
    
    invQ = [invq0, invq1, invq2, invq3]
    return invQ   


#* convert unit Quaternion to angle-axis representation 
def quatToRodrigues(q):
    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3]     
    
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
    
    result = [theta, a1, a2, a3]
    return result
    
    