# Attitude Estimation

Utilizng gyro and accelerometer data from IMU (MPU-6050) to construct attitude estimatior. Then visualize the result wtih Python and OpenGL. This project was initially developed by [mattzzw](https://bit.ly/2TF1jrU). A lot of changes has been made in this separated repo with more detailed descriptions and comments. Furthermore, quaternion version is developed providing singularity-free estimation.


💻 Prerequisite
----------------
### Hardware
1. Arduino Uno (or any 3rd-party compatible baord)
2. GY521 MPU6050

- Interface Arduno with MPU6050
  - 5V -- VCC
  - GND -- GND
  - pin 2 -- INT
  - A4 -- SDA
  - A5 -- SCL

### Python Libraries
1. Pygame
2. PyOpenGL
3. pySerial


🀄️ Projects
----------- 
### visualizer_EulerAngle
Attitude is constructed by z-y-x Euler angles with complementary filter, singluarity exisits. Gyro and accelerometer data are utilized. 

### visualizer_Quaternion
Attitude is constructed by unit quaternions, and then converting to angle-axis rotation. Only gyro data is utilized. 


🎮 Deployment
--------------
1. connect Arduion with MPU-6050 (interfacing diagram can be found [here](https://bit.ly/2VqX6p5))
2. Connect/Power up the Arduino MPU-6050 bundle to PC via USB cable
3. In Arduino IDE 'Tool' tab, select proepr board and port

- For **visualizer_EulerAngle**
4. Uploading firmware (`MPU6050_arduino_firmware.ino`) to Aruuino via Arduino IDE 
5. In any Python IDE, run `_attVisualizer_euler.py` 

- For **visualizer_Quaternion** 
4. Uploading firmware (`MPU6050_arduino_firmware_quat.ino`) to Aruuino via Arduino IDE 
5. run `_attVisualizer_quat.py` in any Python IDE, 

- Memo:  
 code has been tested under the following environment:     
 Arduino IDE 1.8.8  
 Python IDE - Spyder 3.3.2   
 Python 3.7.1, Pygame-1.9.4, PyOpenGL-3.1.0, and  pyserial-3.4   
 ELEGOO UNO 



🤖 Developer
------
Roy T Wu

📚 Ackowledgements
---------------
- https://github.com/mattzzw/Arduino-mpu6050
- https://playground.arduino.cc/Main/MPU-6050
- https://bit.ly/2VqX6p5
- https://www.invensense.com/products/motion-tracking/6-axis/mpu-6050/
