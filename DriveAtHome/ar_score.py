#the main program

import cv2, numpy as np, math, aruco, socket, random,base64
from object_module import *
import sys
import struct
from collision import *
from readmarker import *
from database import *

A = [[1019.37187, 0, 618.709848], [0, 1024.2138, 327.280578], [0, 0, 1]] #hardcoded intrinsic matrix for my webcam
A = np.array(A)
# obj = three_d_object('data/3d_objects/Sphere.1Surface_orange/pumpkin_orange.obj', 'data/3d_objects/Sphere.1Surface_orange/Sphere.1Surface_orange.jpg')
#obj2 = three_d_object('data/3d_objects/lion-cub.obj', 'data/3d_objects/lionfox.png')
obj  = three_d_object('data/3d_objects/foxme.obj', 'data/3d_objects/texture.png')
# obj3  = three_d_object('data/3d_objects/dog/dog.obj', 'data/3d_objects/dog/dog.png')
obj3  = three_d_object('data/3d_objects/pumpkin/pumpkin_green.obj', 'data/3d_objects/pumpkin/Sphere.1Surface_green.jpg')

HOST='192.168.43.159'
#HOST = '192.168.1.104'
# PORT=9999
buffSize=65507

# server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #創建socket對象
# server.bind((HOST,PORT))
# print('adfasfsdf')
# print('now waiting for frames...')

FRAME_HEIGHT = 300
FRAME_WIDTH = 400

def transport(server):
    data,address=server.recvfrom(buffSize) #先接收的是字節長度
    dataA = base64.b64decode(data, ' /')
    npdata = np.fromstring(dataA,dtype=np.uint8)
    frame = cv2.imdecode(npdata, 1)
    return frame

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

def ar_time(player):
	# HOST = '192.168.1.103'
	# HOST = '192.168.1.104'
	HOST = '172.20.10.3'
	PORT=9999

	marker = readmarker('data/marker1.png')
	marker2 = readmarker('data/marker2.png')
	server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #創建socket對象
	server.bind((HOST,PORT))

    
	fps,st,frames_to_count,cnt = (0,0,20,0)

	objNum = 0
	score = 0

	h,w = marker.shape
	#considering all 4 rotations
	sigs = marker_sig(marker)
	sigs2 = marker_sig(marker2)

	frame = transport(server)

	h2, w2, _ = frame.shape
	print(h2, w2)

	h_canvas = max(h, h2)
	w_canvas = w + w2

	times = 0
	ts_ob1 = ts_ob2 = tf_ob1 = tf_ob2 = tcf_ob1 = tcf_ob2 = time.time()

	collision_flag = False
	touch = False
	grayMode = False
	bomb = False
	kk = 0

	#passtimeforthisprocess
	allStart = time.time()
	gameEndTime = time.time()
	#load video
	cap = cv2.VideoCapture('data/effect/Orange_bomb.mov')
	if not cap.isOpened():
		raise IOError("Can't open the video file")
	
	video_start = 0.0
	video_end = 120.0
	time_length = 5.0
	fps = 24
	frame_seq = 0

	cap.set(cv2.CAP_PROP_POS_FRAMES , frame_seq)

	ov, video = cap.read()
	cur_video = cv2.resize(frame,(FRAME_WIDTH,FRAME_HEIGHT), interpolation=cv2.INTER_AREA)

	passScore = 100

	while True:
		frame = transport(server)

		currentTime = time.time()
		elapsedTime = currentTime - allStart

		closedTime = currentTime - gameEndTime

		#frame = np.flip(frame,axis =1)
		augmented = augmented2 = frame
		imgOut = frame
		
		if frame is not None:
			pass
		else:
			continue

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		if ((int(closedTime)  == 3) and score >= 100):
			break

		success, H = aruco.find_homography_aruco(frame, marker, sigs)
		success2, H2 = aruco.find_homography_aruco(frame, marker2, sigs2)
		# success = False

		if (bomb == True and (time.time()-tcf_ob1 <= 5)):
			# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# frame = cv2.flip(frame, 0)
			frame = random_effect(random_seed, frame)
		else:
			bomb = False
			grayMode = False
			kk = 0

		#obj1 is bomb
		if not success:
			if bomb:
				pass
			augmented = augmented2 = augmented_gray  = augmented2_gray  = frame

			collision_flagA = False
		else:
			augmented = augmented2 = augmented_gray  = augmented2_gray  = frame
			R_T = get_extended_RT(A, H)
			transformation = A.dot(R_T) 

			augmented, collision_flagA = augment(frame, obj, transformation, marker, True) #flipped for better control
			if(collision_flagA == True and times == 0):
				ts_ob1 = time.time()
				# print('hhhh')
				times+=1
			elif(collision_flagA == True and times == 1):
				tf_ob1 = time.time()
				if(tf_ob1-ts_ob1 <= 0.25):
					tcf_ob1 = time.time()
					print('congrat A, u touch it!')
					if bomb == False:
						random_seed = random.randint(1,4)
						print(random_seed)
						augmented = random_effect(random_seed, augmented)
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

		#obj2 3 4 is get point object
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
			elif(collision_flagB == True and times == 1):
				tf_ob2 = time.time()
				if(tf_ob2-ts_ob2 <= 0.25):
					print('congrat B, u touch it!')
					touch = True
					score+=10
					if(score == passScore):
						insert_to_time(player, str(int(elapsedTime)), getCurrentTime())
						gameEndTime = time.time()
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
				augmented2 = random_effect(random_seed, augmented2)
				imgOut = cv2.bitwise_or(augmented, augmented2)
				kk+=1
			else:
				imgOut = cv2.bitwise_or(augmented, augmented2)
		else:
			imgOut = cv2.bitwise_or(augmented, augmented2)
		if touch:
			ov, video = cap.read()
			if(ov == True):
				cur_video = cv2.resize(video,(FRAME_WIDTH,FRAME_HEIGHT), interpolation=cv2.INTER_AREA)	
				imgOut = cv2.bitwise_or(imgOut, cur_video)	
			# print(imgOut.shape)
			# print(cur_video.shape)
			elif(ov == False):
				print("video ended")
				touch = False
				cap.set(cv2.CAP_PROP_POS_FRAMES , 0)
				ov, video = cap.read()
				if (ov == False):
					print('video ov')
				cur_video = cv2.resize(video, (FRAME_WIDTH,FRAME_HEIGHT), interpolation=cv2.INTER_AREA)

		imgOut = drawLine(imgOut)
		grayMode = False
			#canvas[:h2 , w: , :] = augmented
		text = 'Your scores:' + str(score)
		timeTest = "Time: " + str(int(elapsedTime))
		cv2.putText(imgOut, text, (10,40), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1, cv2.LINE_AA)
		cv2.putText(imgOut, timeTest, (320,40), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1, cv2.LINE_AA)
		
		cv2.namedWindow('frames', cv2.WINDOW_NORMAL)
		cv2.setWindowProperty('frames', cv2.WND_PROP_FULLSCREEN ,cv2.WINDOW_NORMAL)
		cv2.imshow("frames", imgOut) 

	cv2.destroyAllWindows()

if __name__ == "__main__":
    ar_time("asdf")