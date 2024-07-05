import time
import board

# pip install adafruit-circuitpython-servokit
# pip install adafruit-circuitpython-pca9685
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685


def initHandle():
    for i in range(45):
        servo_handle.angle = 90 - i
        time.sleep(0.005)
    for i in range(90):
        servo_handle.angle = 45 + i
        time.sleep(0.005)
    for i in range(90):
        servo_handle.angle = 135 - i
        time.sleep(0.002)
    for i in range(90):
        servo_handle.angle = 45 + i
        time.sleep(0.002)
    time.sleep(0.3)
    servo_handle.angle = 90


def initCameraLR():
    for i in range(45):
        servo_cameraLR.angle = 80 + i
        time.sleep(0.005)
    for i in range(90):
        servo_cameraLR.angle = 125 - i
        time.sleep(0.005)
    for i in range(45):
        servo_cameraLR.angle = 35 + i
        time.sleep(0.005)


def initCameraUD():
    for i in range(60):
        servo_cameraUD.angle = 180 - i
        time.sleep(0.005)
    time.sleep(0.2)
    for i in range(60):
        servo_cameraUD.angle = 120 + i
        time.sleep(0.005)


def initServo():
    initHandle()  # LEFT 45 - 90 - 135 RIGHT
    time.sleep(0.5)
    initCameraLR()  # LEFT 125 - 80 - 35 RIGHT
    time.sleep(0.2)
    initCameraUD()  # DOWN 60 - 105 UP


i2c = board.I2C()

pca = PCA9685(i2c)
pca.frequency = 50

servo_handle = servo.Servo(pca.channels[0])
servo_cameraLR = servo.Servo(pca.channels[1])
servo_cameraUD = servo.Servo(pca.channels[2])

print("[INFO] Servo initializing..")
initServo()
print("[INFO] Servo initialized!")