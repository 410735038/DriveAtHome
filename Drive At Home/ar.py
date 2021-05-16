#the main program

import cv2
import numpy as np
import math
from object_module import *
import sys
import aruco 
import socket
import struct
import random
from collision import *
from readmarker import *

A = [[1019.37187, 0, 618.709848], [0, 1024.2138, 327.280578], [0, 0, 1]] #hardcoded intrinsic matrix for my webcam
A = np.array(A)
obj = three_d_object('data/3d_objects/foxme.obj', 'data/3d_objects/texture.png')
#obj2 = three_d_object('data/3d_objects/lion-cub.obj', 'data/3d_objects/lionfox.png')
obj3  = three_d_object('data/3d_objects/orange_lowmurcha/Byme.obj', 'data/3d_objects/orange_lowmurcha/Dount_MurchaPicture.png')

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

	#cv2.namedWindow("webcam")
	#vc = cv2.VideoCapture(0)

	h,w = marker.shape
	#considering all 4 rotations
	sigs = marker_sig(marker)
	sigs2 = marker_sig(marker2)
	# marker_sig1 = aruco.get_bit_sig(marker, np.array([[0,0],[0,w], [h,w], [h,0]]).reshape(4,1,2))
	# marker_sig2 = aruco.get_bit_sig(marker, np.array([[0,w], [h,w], [h,0], [0,0]]).reshape(4,1,2))
	# marker_sig3 = aruco.get_bit_sig(marker, np.array([[h,w],[h,0], [0,0], [0,w]]).reshape(4,1,2))
	# marker_sig4 = aruco.get_bit_sig(marker, np.array([[h,0],[0,0], [0,w], [h,w]]).reshape(4,1,2))

	# marker_sig5 = aruco.get_bit_sig(marker2, np.array([[0,0],[0,w], [h,w], [h,0]]).reshape(4,1,2))
	# marker_sig6 = aruco.get_bit_sig(marker2, np.array([[0,w], [h,w], [h,0], [0,0]]).reshape(4,1,2))
	# marker_sig7 = aruco.get_bit_sig(marker2, np.array([[h,w],[h,0], [0,0], [0,w]]).reshape(4,1,2))
	# marker_sig8 = aruco.get_bit_sig(marker2, np.array([[h,0],[0,0], [0,w], [h,w]]).reshape(4,1,2))

	# sigs = [marker_sig1, marker_sig2, marker_sig3, marker_sig4]
	# sigs2 = [marker_sig5, marker_sig6, marker_sig7, marker_sig8]

	frame = transport()

	h2, w2, _ = frame.shape
	print(h2, w2)

	h_canvas = max(h, h2)
	w_canvas = w + w2

	times = 0
	ts_ob1 = ts_ob2 = tf_ob1 = tf_ob2 = tcf_ob1 = tcf_ob2 = time.time()

	collision_flag = False
	c2Gray = False
	c2GrayTime = time.time()
	grayMode = False
	bomb = False
	kk = 0


	while True:
		frame = transport()
		#frame = np.flip(frame,axis =1)
		augmented = augmented2 = frame
		imgOut = frame
		
		if frame is not None:
			#print('have received one frame')
			pass
			#cv2.imshow('frames',frame) #窗口顯示 
		else:
			continue

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		# canvas = np.zeros((h_canvas, w_canvas, 3), np.uint8) #final display
		# canvas[:h, :w, :] = marker_colored #marker for reference

		success, H = aruco.find_homography_aruco(frame, marker, sigs)
		success2, H2 = aruco.find_homography_aruco(frame, marker2, sigs2)
		# print(success, success2)
		# success = False

		if (bomb == True and (time.time()-tcf_ob1 <= 5)):
			# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# frame = cv2.flip(frame, 0)
			frame = random_effect(random_seed, frame)
		else:
			bomb = False
			grayMode = False
			kk = 0

		if not success:
			if bomb:
				pass
			augmented = augmented2 = augmented_gray  = augmented2_gray  = frame
			# print('augmented:', augmented.shape)
			# print('augmented2:', augmented2.shape)
			# print('augmented_gray:', augmented_gray.shape)
			# print('augmented2_gray:', augmented2_gray.shape)
			# augmented = np.array(augmented, dtype = np.uint8)
			collision_flagA = False
			# print('homograpy est failed')
			#canvas[:h2 , w: , :] = np.flip(frame, axis = 1)
			#cv2.imshow("WWW", canvas )
			#continue
		else:
			augmented = augmented2 = augmented_gray  = augmented2_gray  = frame
			R_T = get_extended_RT(A, H)
			transformation = A.dot(R_T) 

			#augmented = np.flip(augment(frame, obj, transformation, marker, True)) #flipped for better control
			#augmented2 = np.flip(augment(frame, obj, transformation2, marker2, True))

			augmented, collision_flagA = augment(frame, obj, transformation, marker, True) #flipped for better control
			if(collision_flagA == True and times == 0):
				ts_ob1 = time.time()
				# print('hhhh')
				times+=1
			elif(collision_flagA == True and times == 3):
				tf_ob1 = time.time()
				if(tf_ob1-ts_ob1 <= 0.25):
					tcf_ob1 = time.time()
					print('congrat A, u touch it!')
					if bomb == False:
						random_seed = random.randint(1,2)
						print(random_seed)
						augmented = random_effect(random_seed, augmented)
						# augmented_gray = cv2.cvtColor(augmented, cv2.COLOR_BGR2GRAY)
						# augmented_flip = cv2.flip(augmented, 0)
						bomb = True
					else:
						pass

					if(score <= 0):
						score = 0
					else:
						score-=10
				times = 0
				# print(times)
			elif(collision_flagA == True):
				t2c_ob1 = time.time()
				if(t2c_ob1-ts_ob1 > 0.5):
					print('over, again!')
					ts_ob1 = t2c_ob1
					times = 1
				else:
					times+=1
	
		if (success2 == False and bomb == True):
			pass
		elif success2 == False and bomb == False:
			pass
		else:
			R_T2 = get_extended_RT(A, H2)
			transformation2 = A.dot(R_T2)

			augmented2, collision_flagB = augment(augmented, obj3, transformation2, marker2, True)

			if(collision_flagB == True and times == 0):
				ts_ob2 = time.time()
				times+=1
			elif(collision_flagB == True and times == 3):
				tf_ob2 = time.time()
				if(tf_ob2-ts_ob2 <= 0.25):
					print('congrat B, u touch it!')
					c2Gray = True
					score+=10
				times = 0
				print(times)
			elif(collision_flagB == True):
				t2c_ob2 = time.time()
				if(t2c_ob2-ts_ob2 > 0.5):
					print('over, again!')
					ts_ob2 = t2c_ob2
					times = 1
				else:
					times+=1
		if bomb:
			if(kk == 0):
				# augmented2_gray = cv2.cvtColor(augmented2, cv2.COLOR_BGR2GRAY)
				# imgOut = cv2.bitwise_or(augmented_gray, augmented2_gray)
				# # augmented2_flip = cv2.flip(augmented2, 0)
				augmented2 = random_effect(random_seed, augmented2)
				imgOut = cv2.bitwise_or(augmented, augmented2)
				kk+=1
			else:
				imgOut = cv2.bitwise_or(augmented, augmented2)
		else:
			imgOut = cv2.bitwise_or(augmented, augmented2)
			# if(time.time() - c2GrayTime > 3):
			# 	c2Gray = False
			# 	augmented2 = cv2.cvtColor(augmented2, cv2.COLOR_GRAY2BGR)

		# if(c2Gray == True):
		# 	augmented_gray = cv2.cvtColor(augmented, cv2.COLOR_GRAY2BGR)
		# 	imgOut = cv2.bitwise_or(augmented_gray, augmented2_gray)
		# elif(c2Gray == False):

		# print(augmented_gray.shape, augmented2_gray.shape)
		# imgOut = cv2.bitwise_or(augmented, augmented2)

		imgOut = drawLine(imgOut)
		grayMode = False
			#canvas[:h2 , w: , :] = augmented
		text = 'Your scores:' + str(score)
		cv2.putText(imgOut, text, (10,40), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0,255,255), 1, cv2.LINE_AA)
		
		cv2.namedWindow('frames', cv2.WINDOW_NORMAL)
		cv2.setWindowProperty('frames', cv2.WND_PROP_FULLSCREEN ,cv2.WINDOW_NORMAL)
		cv2.imshow("frames", imgOut) 

	cv2.destroyAllWindows()
if __name__ == '__main__':
	main()
