import cv2
import time
import poseModule as pm
import math

def steering_angle(x1, y1, x2, y2):
    if (x2 - x1 == 0):
        angle = 0.0
    else:
        m = (y2 - y1) / (x2 - x1)
        angle = math.degrees(math.atan(m))
    return angle

def move_speed(x):
    #car speed stuff
    # if(x>=200):
    #     print("car speed: 200")
    # elif(x<200 and x>=150):
    #     print("car speed: 150")
    print('speed:', x)


cap =  cv2.VideoCapture(0)
success, first = cap.read()
print(first.shape)
pTime = 0
detector = pm.poseDetector()
while True:
    success, frame = cap.read()
    frame = detector.findPose(frame)
    lmList = detector.findPosition(frame, draw=False)
    if len(lmList) != 0:
        # print(lmList[24])
        cv2.circle(frame, (lmList[0][1], lmList[0][2]), 15, (0,0,255), cv2.FILLED)
    try:
        #lh
        if lmList[15][2] < lmList[0][2] - 30:
            # print("raise left hand")
            #rotate
            if(lmList[28][2]<480):
                print(steering_angle(lmList[15][1], lmList[15][2], lmList[28][1], lmList[28][2]) )
        #rh
        if lmList[16][2] < lmList[0][2] - 30:        
            # print("raise right hand")
            if(lmList[27][2]<480):
                steering_angle(lmList[16][1], lmList[16][2], lmList[27][1], lmList[27][2]) 
        # sit 
        if (abs(lmList[24][2] - lmList[26][2]) < 60) and (abs(lmList[23][2] - lmList[25][2]) < 60):
            print("sit")  
        #squat
        if (abs(lmList[24][2] - lmList[26][2]) < 100) and (abs(lmList[23][2] - lmList[25][2]) < 100):
            print("squat")      

        if(lmList[27][2]<480 and lmList[28][2]<480):
            if(abs(lmList[27][1]-lmList[28][1] > 50)):
                move_speed(abs(lmList[27][1]-lmList[28][1]))
    except:
        print("angle wrong")
     
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    try:
        if(lmList[16][1] <= 640 and lmList[16][2] <= 480 and lmList[27][1] <= 640 and lmList[27][2] <= 480):
            cv2.line(frame, (lmList[16][1], lmList[16][2]), (lmList[27][1], lmList[27][2]), (0,0,255), 4)
        if(lmList[15][1] <= 640 and lmList[15][2] <= 480 and lmList[28][1] <= 640 and lmList[28][2] <= 480):
            cv2.line(frame, (lmList[15][1], lmList[15][2]), (lmList[28][1], lmList[28][2]), (0,0,255), 4)   
    except:
        print("cant find angle")
    
    cv2.putText(frame, str(int(fps)), (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.imshow("pose", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows