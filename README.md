# Attitude Estimation

Using gyro and accelerometer data from IMU (MPU-6050) with the help of Arduino and Python to construct an attitude estimator


💻 Prerequisite
----------------
### Hardware
1. Arduino Uno (or 3rd-party compatible baord)
2. GY521 MPU 6050

### Python Libraries
1. Pygame
2. PyOpenGL
3. pySerial


🎮 Deployment
--------------
1. connect Arduion with MPU-6050 (connection diagram can be found at https://bit.ly/2VqX6p5)
2. Connect/Power up the Arduino MPU-6050 bundle to PC via USB cable
3. In Arduino IDE 'Tool' tab, select proepr board and port 
4. Uploading firmware to Aruuino via Arduino IDE
5. In any Python IDE, run boxctrl_6d0f_imu.py


 - Memo:  
 code has been tested under the following environment:     
 Arduino IDE 1.8.8  
 Python IDE - Spyder 3.3.2   
 Python 3.7.1, Pygame-1.9.4, PyOpenGL-3.1.0, and  pyserial-3.4



🤖 Author 
------
Roy T Wu

📚 Ackowledgements
---------------
- https://github.com/mattzzw/Arduino-mpu6050
- https://playground.arduino.cc/Main/MPU-6050
- https://bit.ly/2VqX6p5
- https://www.invensense.com/products/motion-tracking/6-axis/mpu-6050/
