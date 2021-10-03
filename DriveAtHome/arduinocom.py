
from ctypes.wintypes import CHAR
import serial
import time


class ArduinoConnector:
    defaultPort = 'COM7'

    def __init__(self, port=defaultPort):
        self.baudrate = 9600
        self.port = port
        self.arduino = None
        self.initialized = False
        self.last_speed = self.last_direction = chr(126)
        self.last_steer = 0

    """
    Takes the given char and sends it thru serial
    """

    def writeChar(self, mesg):
        mesg = str(mesg)
        if self.initialized:
            self.arduino.write(mesg.encode('utf-8'))

    """
    Takes a speed in range [0,100] and sends it
    """

    def SetSpeed(self, speed):
        if speed is not None:
            # print("Try to SET SPEED " + str(speed))
            sp = chr(int(self.map(speed, 0, 100, 48, 57)))

            if not sp == self.last_speed:
                self.last_speed = sp
                print(self.last_speed)
                self.writeChar(sp)
            if self.last_speed == sp:
                self.writeChar(sp)

    def Stop(self):
        if not self.last_direction == 'S':
            self.last_direction = 'S'
            self.writeChar('S')
        if self.last_direction == 'S':
            self.writeChar('S')
            self.SetSpeed(0)

    def Forward(self):
        if not self.last_direction == 'F':
            self.last_direction = 'F'
            self.writeChar('F')
        if self.last_direction == 'F':
            self.writeChar('F')

    def LeftForward(self):
        # print("GGGGGGGGGGGGGGGGGGGGGGGGGGGG")
        if not self.last_direction == 'G':
            self.last_direction = 'G'
            self.writeChar('G')
        if self.last_direction == 'G':
            # print("gggggggggggggggggggggggggg")
            self.writeChar('G')

    def RightForward(self):
        if not self.last_direction == 'I':
            self.last_direction = 'I'
            self.writeChar('I')
        if self.last_direction == 'I':
            self.writeChar('I')

    def Backward(self):
        if not self.last_direction == 'B':
            self.last_direction = 'B'
            self.writeChar('B')
        if self.last_direction == 'B':
            self.writeChar('B')

    def LeftBackward(self):
        if not self.last_direction == 'H':
            self.last_direction = 'H'
            self.writeChar('H')
        if self.last_direction == 'H':
            self.writeChar('H')

    def RightBackward(self):
        if not self.last_direction == 'J':
            self.last_direction = 'J'
            self.writeChar('J')
        if self.last_direction == 'J':
            self.writeChar('J')

    """
        Takes a steer value in range [-90,90] and sends it correctly
    """

    def Steer(self, angle):
        coeff = round(self.map(angle, 0, 90, 5, 10))
        self.writeChar(coeff)

    def initialize(self):
        self.arduino = serial.Serial(self.port, self.baudrate)
        time.sleep(2)
        self.initialized = True

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def disconnect(self):
        self.arduino.close()