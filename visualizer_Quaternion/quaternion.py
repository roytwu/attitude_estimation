"""
Developer:   Roy TWu
File Name:   quaternion.py
Description: Custom module about quaternion multiplication
"""

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