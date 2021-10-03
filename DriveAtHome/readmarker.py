import cv2
import aruco
import numpy as np

def readmarker(filepath):
    marker_colored = cv2.imread(filepath)
    marker_colored =  cv2.resize(marker_colored, (480,480), interpolation = cv2.INTER_CUBIC )
    marker = cv2.cvtColor(marker_colored, cv2.COLOR_BGR2GRAY)
    return marker

def marker_sig(marker):
    h,w = marker.shape
    marker_sig1 = aruco.get_bit_sig(marker, np.array([[0,0],[0,w], [h,w], [h,0]]).reshape(4,1,2))
    marker_sig2 = aruco.get_bit_sig(marker, np.array([[0,w], [h,w], [h,0], [0,0]]).reshape(4,1,2))
    marker_sig3 = aruco.get_bit_sig(marker, np.array([[h,w],[h,0], [0,0], [0,w]]).reshape(4,1,2))
    marker_sig4 = aruco.get_bit_sig(marker, np.array([[h,0],[0,0], [0,w], [h,w]]).reshape(4,1,2))
    sigs = [marker_sig1, marker_sig2, marker_sig3, marker_sig4]
    return sigs

def drawLine(imgOut):
    cv2.line(imgOut, (100-20,75), (300+20,75), (0,0,255), 3) #top
    cv2.line(imgOut, (140,35), (140,225), (0,0,255), 3) #left
    cv2.line(imgOut, (260,35), (260,225), (0,0,255), 3) #right
    cv2.line(imgOut, (100-20,175), (320,175), (0,0,255), 3) #bottom
    return imgOut