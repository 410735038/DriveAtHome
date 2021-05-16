#the main program

import cv2
import numpy as np
import math
from object_module import *
import sys
import aruco 
import socket
import struct
from collision import *
from readmarker import *

A = [[1019.37187, 0, 618.709848], [0, 1024.2138, 327.280578], [0, 0, 1]] #hardcoded intrinsic matrix for my webcam
A = np.array(A)
obj = three_d_object('data/3d_objects/fox.obj', 'data/3d_objects/texture.png')
#obj2 = three_d_object('data/3d_objects/lion-cub.obj', 'data/3d_objects/lionfox.png')
obj3  = three_d_object('data/3d_objects/orange/car_wheelByme.obj', 'data/3d_objects/orange/car_ver2.png')

HOST='134.208.35.128'
PORT=9999
buffSize=65507

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

def main():
	marker = readmarker('data/marker1.png')
	marker2 = readmarker('data/marker2.png')

	objNum = 0
	score = 0

	h,w = marker.shape
	#considering all 4 rotations
	sigs = marker_sig(marker)
	sigs2 = marker_sig(marker2)

	frame = transport()
	h2, w2, _ = frame.shape
	print(h2, w2)

	h_canvas = max(h, h2)
	w_canvas = w + w2

	times = 0
	ts = tf = time.time()

	collision_flag = False


	while True:
		#frame = transport() #fetch frame from webcam

		frame = transport()
		augmented = frame
		imgOut = frame
		
		if frame is not None:
			pass
		else:
			continue

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


		success, H = aruco.find_homography_aruco(frame, marker, sigs)
		success2, H2 = aruco.find_homography_aruco(frame, marker2, sigs2)
		if not success:
			augmented = frame
			collision_flag = False
		else:
			R_T = get_extended_RT(A, H)
			transformation = A.dot(R_T) 

			augmented, collision_flag = augment(frame, obj3, transformation, marker, True) #flipped for better control
			if(collision_flag == True and times == 0):
				ts = time.time()
				times+=1
			elif(collision_flag == True and times == 3):
				tf = time.time()
				if(tf-ts <= 0.25):
					print('congrat, u touch it!')
					score+=10
				times = 0
				print(times)
			elif(collision_flag == True):
				t2c = time.time()
				if(t2c-ts > 0.5):
					print('over, again!')
					ts = t2c
					times = 1
				else:
					times+=1

			

		if not success2:
			augmented2 = frame
			collision_flag = False
		else:
			R_T2 = get_extended_RT(A, H2)
			transformation2 = A.dot(R_T2)

			augmented2, collision_flag = augment(augmented, obj, transformation2, marker2, True)
			if(collision_flag == True and times == 0):
				ts = time.time()
				times+=1
			elif(collision_flag == True and times == 3):
				tf = time.time()
				if(tf-ts <= 0.25):
					print('congrat, u touch it!')
					score+=10
				times = 0
				print(times)
			elif(collision_flag == True):
				t2c = time.time()
				if(t2c-ts > 0.5):
					print('over, again!')
					ts = t2c
					times = 1
				else:
					times+=1
		
		imgOut = cv2.bitwise_or(augmented, augmented2)
		imgOut = drawLine(imgOut)

		text = 'Your scores:' + str(score)
		cv2.putText(imgOut, text, (10,40), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0,255,255), 1, cv2.LINE_AA)
		
		cv2.namedWindow('frames', cv2.WINDOW_NORMAL)
		cv2.setWindowProperty('frames', cv2.WND_PROP_FULLSCREEN ,cv2.WINDOW_NORMAL)
		cv2.imshow("frames", imgOut) 

	cv2.destroyAllWindows()
if __name__ == '__main__':
	main()
