#the main program

import cv2
import numpy as np
import math
from object_module import *
import sys
import aruco 
import socket
import struct

A = [[1019.37187, 0, 618.709848], [0, 1024.2138, 327.280578], [0, 0, 1]] #hardcoded intrinsic matrix for my webcam
A = np.array(A)
obj = three_d_object('data/3d_objects/fox.obj', 'data/3d_objects/texture.png')
#obj2 = three_d_object('data/3d_objects/lion-cub.obj', 'data/3d_objects/lionfox.png')

HOST='134.208.35.128'
PORT=9999
buffSize=65535

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #創建socket對象
server.bind((HOST,PORT))
print('now waiting for frames...')

def transport():
    data,address=server.recvfrom(buffSize) #先接收的是字節長度
    if len(data)==1 and data[0]==1: #如果收到關閉消息則停止程序
        server.close()
        cv2.destroyAllWindows()
        exit()
    if len(data)!=4: #進行簡單的校驗，長度值是int類型，佔四個字節
        length=0
    else:
        length=struct.unpack('i',data)[0] #長度值
    data,address=server.recvfrom(buffSize) #接收編碼圖像數據
    #if length!=len(data): #進行簡單的校驗
        #continue
    data=np.array(bytearray(data)) #格式轉換
    imgdecode=cv2.imdecode(data,1) #解碼
    #print('have received one frame')
    return imgdecode

def get_extended_RT(A, H):
	#finds r3 and appends
	# A is the intrinsic mat, and H is the homography estimated
	H = np.float64(H) #for better precision
	A = np.float64(A)
	R_12_T = np.linalg.inv(A).dot(H)

	r1 = np.float64(R_12_T[:, 0]) #col1
	r2 = np.float64(R_12_T[:, 1]) #col2
	T = R_12_T[:, 2] #translation
	
	#ideally |r1| and |r2| should be same
	#since there is always some error we take square_root(|r1||r2|) as the normalization factor
	norm = np.float64(math.sqrt(np.float64(np.linalg.norm(r1)) * np.float64(np.linalg.norm(r2))))
	
	r3 = np.cross(r1,r2)/(norm)
	R_T = np.zeros((3, 4))
	R_T[:, 0] = r1
	R_T[:, 1] = r2 
	R_T[:, 2] = r3 
	R_T[:, 3] = T
	return R_T

def hello():
	marker_colored = cv2.imread('data/marker1.png')
	marker_colored =  cv2.resize(marker_colored, (480,480), interpolation = cv2.INTER_CUBIC )
	marker = cv2.cvtColor(marker_colored, cv2.COLOR_BGR2GRAY)

	marker_colored2 = cv2.imread('data/marker2.png')
	marker_colored2 =  cv2.resize(marker_colored2, (480,480), interpolation = cv2.INTER_CUBIC )
	marker2 = cv2.cvtColor(marker_colored2, cv2.COLOR_BGR2GRAY)


	#cv2.namedWindow("webcam")
	#vc = cv2.VideoCapture(0)

	h,w = marker.shape
	#considering all 4 rotations
	marker_sig1 = aruco.get_bit_sig(marker, np.array([[0,0],[0,w], [h,w], [h,0]]).reshape(4,1,2))
	marker_sig2 = aruco.get_bit_sig(marker, np.array([[0,w], [h,w], [h,0], [0,0]]).reshape(4,1,2))
	marker_sig3 = aruco.get_bit_sig(marker, np.array([[h,w],[h,0], [0,0], [0,w]]).reshape(4,1,2))
	marker_sig4 = aruco.get_bit_sig(marker, np.array([[h,0],[0,0], [0,w], [h,w]]).reshape(4,1,2))

	marker_sig5 = aruco.get_bit_sig(marker2, np.array([[0,0],[0,w], [h,w], [h,0]]).reshape(4,1,2))
	marker_sig6 = aruco.get_bit_sig(marker2, np.array([[0,w], [h,w], [h,0], [0,0]]).reshape(4,1,2))
	marker_sig7 = aruco.get_bit_sig(marker2, np.array([[h,w],[h,0], [0,0], [0,w]]).reshape(4,1,2))
	marker_sig8 = aruco.get_bit_sig(marker2, np.array([[h,0],[0,0], [0,w], [h,w]]).reshape(4,1,2))

	sigs = [marker_sig1, marker_sig2, marker_sig3, marker_sig4]
	sigs2 = [marker_sig5, marker_sig6, marker_sig7, marker_sig8]

	frame = transport()
	h2, w2, _ = frame.shape
	print(h2, w2)

	h_canvas = max(h, h2)
	w_canvas = w + w2

	


	while True:
		#frame = transport() #fetch frame from webcam

		frame = transport()
		#frame = np.flip(frame,axis =1)
		augmented = frame
		imgOut = frame
		
		if isinstance(len(frame),int) == True:
			#print('have received one frame')
			pass
			#cv2.imshow('frames',frame) #窗口顯示 
		else:
			continue

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		canvas = np.zeros((h_canvas, w_canvas, 3), np.uint8) #final display
		canvas[:h, :w, :] = marker_colored #marker for reference

		success, H = aruco.find_homography_aruco(frame, marker, sigs)
		success2, H2 = aruco.find_homography_aruco(frame, marker2, sigs2)
		# success = False
		if not success:
			i = 0
			# print('homograpy est failed')
			#canvas[:h2 , w: , :] = np.flip(frame, axis = 1)
			#cv2.imshow("WWW", canvas )
			#continue
		else:
			R_T = get_extended_RT(A, H)
			transformation = A.dot(R_T) 

			R_T2 = get_extended_RT(A, H2)
			transformation2 = A.dot(R_T2)
		
			#augmented = np.flip(augment(frame, obj, transformation, marker, True)) #flipped for better control
			#augmented2 = np.flip(augment(frame, obj, transformation2, marker2, True))

			augmented = augment(frame, obj, transformation, marker, True) #flipped for better control
			augmented2 = augment(augmented, obj, transformation2, marker2, True)

			imgOut = cv2.bitwise_or(augmented, augmented2)


			
			#canvas[:h2 , w: , :] = augmented
		cv2.line(imgOut, (120,120), (520,120), (0,0,255), 3)
		cv2.line(imgOut, (120,360), (520,360), (0,0,255), 3)
		cv2.line(imgOut, (160,80), (160,400), (0,0,255), 3)
		cv2.line(imgOut, (480,80), (480,400), (0,0,255), 3)
		
		cv2.namedWindow('frames', cv2.WINDOW_NORMAL)
		cv2.setWindowProperty('frames', cv2.WND_PROP_FULLSCREEN ,cv2.WINDOW_NORMAL)
		cv2.imshow("frames", imgOut) 

	cv2.destroyAllWindows()
if __name__ == '__main__':
	main()
