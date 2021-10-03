import cv2, numpy as np, socket,base64
from object_module import *
from collision import *
from readmarker import *
from database import *

# HOST='134.208.35.128'
# HOST = '192.168.1.103'
# PORT=9999
buffSize=65507

# server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #創建socket對象
# server.bind((HOST,PORT))
# print('now waiting for frames...')

def transport(server):
    data,address=server.recvfrom(buffSize) #先接收的是字節長度
    dataA = base64.b64decode(data, ' /')
    npdata = np.fromstring(dataA,dtype=np.uint8)
    frame = cv2.imdecode(npdata, 1)
    return frame

def free(player): 	
	HOST = '172.20.10.3'
	PORT=9999
	server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #創建socket對象
	server.bind((HOST,PORT))
	frame = transport(server)

	h2, w2, _ = frame.shape
	print(h2, w2)


	while True:
		frame = transport(server)

		
		if frame is not None:
			pass
		else:
			continue

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		cv2.namedWindow('frames', cv2.WINDOW_NORMAL)
		cv2.setWindowProperty('frames', cv2.WND_PROP_FULLSCREEN ,cv2.WINDOW_NORMAL)
		cv2.imshow("frames", frame) 

	cv2.destroyAllWindows()