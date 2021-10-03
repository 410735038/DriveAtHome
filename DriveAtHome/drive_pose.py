#!/usr/bin/python
import os
import sys
import time
from sys import *
import numpy as np
import cv2
import math
from SerialManager import ConnectToSerial
from Utils import parseArgs
#--- import mediapipe and mypose module
import poseModule as pm


sendCommandsToCar, source, args = parseArgs()

# Front direction min and max angle
min_angle_front = -3
max_angle_front = 3

# Steering direction. Change to flip directions
# FLIP_STEER = args.flip_steer

# Optimization for steer and speed.
# Higher means safer but much more noise-affected
SPEED_MAX_VARIATION = 150
STEER_MAX_VARIATION = 90

right_UI_status_X = 520

# Colors for steering line
steer_front = (0, 255, 0)
steer_right = (255, 0, 0)
steer_left = (255, 0, 0)

# Global using vars

# Max y speed on CAM, (MAX value = 380)
MAX_SPEED_Y = 200
# Car state: 0 (stop), 1 (go) (INT)
status = 0
last_status = 0
# Car selected direction: 1 (backward), 2 (forward) (INT)
selected_direction = 0
# Steering Angle
steeringAngle = 0.0
_last_angle = 0.0
# Speed
speed = 0
last_speed = 0
# Car connector
carSerial = None

# Counter for errors in body. 1 means fps count. 0.5 means a half of fps count....
MAX_OP_MULTIPLIER = .8

# moving average filter parameter
# alpha regulates the update speed (how fast the accumulator “forgets” about earlier images)
alpha = 0.8

def main():
    #create mediapipe pose object
    detector = pm.poseDetector()

    global speed, steeringAngle, status, last_status, selected_direction, carSerial, alpha, MAX_OP_MULTIPLIER
    # Starting serial esp8266 connection
    if sendCommandsToCar:
        carSerial = ConnectToSerial()
        if carSerial is None:
            print("No port selected, exiting...")
            #sys.exit(-2)
            return "no port selected."
        elif (carSerial == -1):
            return -1 # to end this function
        
    #in ui if get -1 then show connect failed.
            
        
    #if success find will show the window to play.

    # Start webcam with VideoCapture. 0 -> use default webcam
    # WINDOWS_NORMAL dynamic window resize at running time
    # resizeWindow output windows webcam dimension. RESOLUSpeedsTION -> 4:3
    cv2.namedWindow('OPtoROBO', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('OPtoROBO', 1000, 750)
    stream = cv2.VideoCapture(0)
    time.sleep(2)
    if stream is None:
        print("No stream at " + str(0))
        sys.exit(-3)
    if not stream.isOpened():
        print("Stream at " + str(0) + " unvailable. Unable to open.")
        sys.exit(-4)

    # Frame counter
    counter = 0
    # Execution time
    start = time.time()
    fps = 0.0
    fps_last_time = time.time() - 1000
    fps_last_counter = counter - 1
    quit_count = 0

    error_op_counter = 0

    # moving average filter
    ret, img = stream.read()
    avg = np.float32(img)

    while True:
        # Update fps
        if counter % 5 == 1:
            fps = (counter - fps_last_counter) / (time.time() - fps_last_time)
            fps_last_time = time.time()
            fps_last_counter = counter

        # Frame reader. Each frame will be processed by OpenPose
        ret, img = stream.read()

        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        # Output flip
        # cv2.flip(img, 1, img)

        # Bilateral Filtering
        img = cv2.bilateralFilter(img, 9, 40, 75)


        # ---------------------------------------------------
        # Detecting people control
        
        steeringAngle = steering_angle(lmList[16][1], lmList[16][2],
                                       lmList[15][1], lmList[15][2])

        # Direction and Stop
        # if both hands up 
        # shoule use higher than nose
        if (lmList[15][1] < 380 or lmList[16][1] < 380) and selected_direction != 0:
            # Go time
            status = 1
        else:
            # if one or both hands down into command part
            status = 0
            Stop()
            if (380 < lmList[15][2] < 480 and 0 < lmList[15][1] < 160
                    and lmList[16][2] > 380):
                selected_direction = 1
                print('<-------BACKWARD', status)
            elif (380 < lmList[16][2] < 480 and 480 < lmList[16][1] < 640
                  and lmList[15][2] > 380):
                selected_direction = 2
                print('FORWARD-------->', status)
            elif (((lmList[15][2] > 380.0 and lmList[16][2] > 380.0) or (
                    lmList[15][2] == 0.0
                    and lmList[16][2] == 0.0) or
                   (lmList[15][2] == 0.0 and lmList[16][2] > 380.0)
                   or (lmList[15][2] > 380.0 and lmList[16][2] == 0.0))
                  and (160 < lmList[15][1] < 640 and 0 < lmList[16][1] < 480)
                  or (lmList[15][1] == 0.0 and lmList[16][1] == 0.0)):
                speed = 0
                Stop()
                print('------STOP------', status)

        # If we just exited from stop zone, a Forward of Backward call is needed
        if status == 1 and last_status == 0:
            if selected_direction == 1:
                Backward()
            elif selected_direction == 2:
                Forward()
        # if last_status == 1 and status == 0:
        #    selected_direction = 0

        # Gestures detection
        if status == 1:
            speed = int(speed_value(
                lmList[16][2], lmList[15][2]))
            if speed < 0:
                speed = 0
            if (min_angle_front < steeringAngle < max_angle_front and lmList[16][2] < 380.0 and lmList[15][2] < 380.0):
                print('----FRONT----. STATUspeedMS: ', status_to_str(),
                      '. SPEED:  ', speed, '. ANGLE: ', 0)
                    #   F+speed
                sendSpeed()
                if selected_direction == 1:
                    Backward()
                elif selected_direction == 2:
                    Forward()
            else:
                if (max_angle_front < steeringAngle < 90.0 and lmList[16][2] < 380.0
                        and lmList[15][2] < 380.0):
                    # L+speed
                    print('LEFT---------. STATUS: ', status_to_str(), '. SPEED:  ', speed, '. ANGLE: ',
                          round(steeringAngle, 2))
                    sendSpeed()
                    Steer()
                    # if FLIP_STEER:
                    #     steeringAngle = -steeringAngle
                    if selected_direction == 1:
                        LeftBackward()
                    elif selected_direction == 2:
                        LeftForward()
                    # Steer()
                else:
                    if (-90.0 < steeringAngle < min_angle_front and lmList[16][2] < 380.0
                            and lmList[15][2] < 380.0):
                        # R+speed
                        print('--------RIGHT. STATUS: ', status_to_str(), '. SPEED:  ', speed, '. ANGLE: ',
                              round(steeringAngle, 2))
                        sendSpeed()
                        Steer()
                        if selected_direction == 1:
                            RightBackward()
                        elif selected_direction == 2:
                            RightForward()
                        
                        # if FLIP_STEER:
                        #     steeringAngle = -steeringAngle
                        # Steer()

        # Output with OpenPose skeleton
        # Show line between hands
        steer_color = steer_front
        if steeringAngle < min_angle_front:
            steer_color = steer_left
        if steeringAngle > max_angle_front:
            steer_color = steer_right
        if not lmList[16][1] == 0 and not lmList[15][1] == 0:
            cv2.line(img, pt1=(int(lmList[16][1]), int(lmList[16][2])),
                     pt2=(int(lmList[15][1]), int(lmList[15][2])), color=steer_color, thickness=5)

        # Stop Line
        cv2.line(img, (160, 380), (480, 380), (0, 0, 255), thickness=3)
        cv2.putText(img, 'STOP', (260, 420),
                    cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 255), thickness=2)
        cv2.putText(img, 'B', (65, 420), cv2.FONT_HERSHEY_TRIPLEX,
                    1.5, (0, 255, 0), thickness=2)
        cv2.putText(img, 'F', (545, 420), cv2.FONT_HERSHEY_TRIPLEX,
                    1.5, (255, 0, 0), thickness=2)
        # Show speedometer
        cv2.putText(img, "SPD: " + str(speed), (right_UI_status_X, 30), cv2.FONT_HERSHEY_TRIPLEX, .5, (0, 0, 0),
                    thickness=2)
        # Show Speed ui
        cv2.rectangle(img, (610, (370 - speed)),
                      (630, 370), (0, 255, 0), thickness=-2)
        # Show steerAngle
        cv2.putText(img, "STR: " + str(int(steeringAngle)), (right_UI_status_X, 60), cv2.FONT_HERSHEY_TRIPLEX, .5,
                    (0, 0, 0),
                    thickness=2)
        # Show Fps
        cv2.putText(img, "FPS: " + str(round(fps, 1)), (right_UI_status_X, 90), cv2.FONT_HERSHEY_TRIPLEX, .5,
                    (0, 0, 0),
                    thickness=2)
        # Show Mode
        if status == 0:
            cv2.putText(img, 'STOP MODE', (20, 30),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 255), thickness=2)
            if selected_direction == 1:
                cv2.putText(img, 'BACKWARD', (170, 30),
                            cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
            elif selected_direction == 2:
                cv2.putText(img, 'FORWARD', (170, 30),
                            cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
        elif status == 1:
            cv2.putText(img, 'GO MODE', (20, 30),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), thickness=2)
            if selected_direction == 1:
                cv2.putText(img, 'BACKWARD', (170, 30),
                            cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
            elif selected_direction == 2:
                cv2.putText(img, 'FORWARD', (170, 30),
                            cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
        # Quitting progress bar
        if quit_count != 0:
            cv2.putText(img, ' Quitting...', (10, 60),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), thickness=2)
            cv2.rectangle(img, (22, 70), (122, 90), (0, 255, 0), thickness=-2)
            cv2.rectangle(img, (22 + 10 * quit_count, 70),
                          (122, 90), (255, 255, 255), thickness=-2)

        # Backward/Forward zones
        cv2.rectangle(img, (0, 380), (160, 480), (0, 255, 0), thickness=2)
        cv2.rectangle(img, (480, 380), (640, 480), (255, 0, 0), thickness=2)

        # img = imshow_img(img, avg, alpha)

        cv2.imshow('OPtoROBO', img)

        if speed >= 370:
            c = 0

        counter = counter + 1
        last_status = status

        # Quit gesture
        try:
            if (380 < lmList[15][2] < 480 and 0 < lmList[15][1] < 160
                    and 380 < lmList[16][2] < 480 and 480 < lmList[16][1] < 640):
                cv2.rectangle(img, (160, 400), (480, 420),
                              (0, 255, 0), thickness=2)
                quit_count = quit_count + 1
                if quit_count > 10:
                    break
            else:
                quit_count = 0
        except Exception as e1:
            print(e1)
            c = 0

        # q, Q == quit, STOP SCRIPT; NB: waitKey MUST BE 1
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            break

    end = time.time()
    # Resources release
    stream.release()
    cv2.destroyAllWindows()
    total_time = end - start

    # Time and fps
    print(
        '-----------------------------------------------------------------------------------------------------------')
    print('Total script execution time : ', total_time)
    print('FPS: ', counter / total_time)
    print(
        '-----------------------------------------------------------------------------------------------------------')


# Utils
def status_to_str():
    global status
    if status == 0:
        return "STOP"
    if status == 1:
        return "BACKWARD"
    if status == 2:
        return "FORWARD"
    return "UNKNOWN"


# Steering functions
def steering_angle(x1, y1, x2, y2):
    if (x2 - x1 == 0):
        angle = 0.0
    else:
        m = (y2 - y1) / (x2 - x1)
        angle = math.degrees(math.atan(m))
    return angle


def speed_value(y1, y2):
    average_wirsts = (y1 + y2) / 2
    average_wirsts -= 10
    if average_wirsts < 0:
        average_wirsts = 0
    speed = 370 - average_wirsts
    return speed


# Commands to Controller
def sendSpeed():
    global last_speed, speed, MAX_SPEED_Y
    optimize_speed()
    if sendCommandsToCar:
        if speed > MAX_SPEED_Y:
            carSerial.SetSpeed(100)
        else:
            carSerial.SetSpeed(int(speed / (MAX_SPEED_Y / 100)))
    last_speed = speed



def optimize_speed():
    global speed, last_speed, SPEED_MAX_VARIATION
    if args.unoptimized_speed:
        return
    if abs(last_speed - speed) > SPEED_MAX_VARIATION:
        speed = last_speed


def Backward():
    if sendCommandsToCar:
        carSerial.Backward()
def LeftBackward():
    if sendCommandsToCar:
        carSerial.LeftBackward()
def RightBackward():
    if sendCommandsToCar:
        carSerial.RightBackward()


def Forward():
    if sendCommandsToCar:
        carSerial.Forward()
def LeftForward():
    if sendCommandsToCar:
        carSerial.LeftForward()
def RightForward():
    if sendCommandsToCar:
        carSerial.RightForward()


def Stop():
    if sendCommandsToCar:
        carSerial.Stop()


def Steer():
    global _last_angle, steeringAngle

    optimize_steering()
    if sendCommandsToCar:
        carSerial.Steer(steeringAngle)
    _last_angle = steeringAngle


def optimize_steering():
    global steeringAngle, _last_angle, STEER_MAX_VARIATION
    if args.unoptimized_steer:
        return
    if abs(_last_angle - steeringAngle) > STEER_MAX_VARIATION:
        steeringAngle = _last_angle


def imshow_img(img, avg, alpha):
    if args.moving_average_filter:
        cv2.accumulateWeighted(img, avg, alpha)
        res = cv2.convertScaleAbs(avg)
        return res
    else:
        return img



if __name__ == "__main__":
    main()
