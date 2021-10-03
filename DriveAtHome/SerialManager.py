
from arduinocom import ArduinoConnector
from sys import platform
import glob
import serial
# from Connecttest02 import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog, QApplication
from Dialog_connect import Ui_Dialog_connect

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif platform.startswith('linux') or platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def ConnectToSerial(square):
    #車子連接中要放在這喔
    #####
    # print("sssssssssssssss")
    # square.show()
    ports = serial_ports()
    if ports == None or len(ports) == 0:
        #show unavailable find ports widget.
        print('Unable to find available ports')
        return -1
        #exit()
    port = choosePort(ports)
    connector = ArduinoConnector(port)
    print('Initializing serial port...')
    connector.initialize()

    # print("qqqqqqqqqqqqqqqq")
    # square.close()

    #stop looping
    return connector


def choosePort(ports):
    #show widget to choose port in here.
    exit = False
    selected_index = 0
    while not exit:
        #dynamic show widget and choose, we can use ports array to show checkbox
        # for i, p in enumerate(ports):
        #     #dynamic show
        #     #selected_index = show(ports)
        #     print('Port ' + str(i) + ": " + str(p))
        # number = input("Choose the port (type number): ")
        try:
            selected_index = int(1)
            # selected_index = int(number)
            if 0 <= selected_index < len(ports):
                exit = True
        except ValueError:
            pass
    return ports[selected_index]

