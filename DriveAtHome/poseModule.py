import cv2
import mediapipe as mp
import time

from mediapipe.python.solutions import pose

class poseDetector():
    def __init__(self, mode = False, upBody = False, smooth = True, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.upBody,self.smooth,self.detectionCon,self.trackCon)
    
    def findPose(self, img, draw=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        #print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm) 
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255,0,0), cv2.FILLED)
        return lmList
        """
        the result(x, y, z) of lm from every id is the ratio of img
        ex: x:0.15 y:0.9 z:0.15
        it means if the height and width of image is 480, 640
        ratio of x is value/480 = 0.15
        so if we want to get the practical value of x and y axis in the image
        we can let x and y multiple the height and width 
        """
 
def main():
    cap =  cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()
    while True:
        success, frame = cap.read()
        frame = detector.findPose(frame)
        lmList = detector.findPosition(frame, draw=False)
        if len(lmList) != 0:
            print(lmList[0])
            cv2.circle(frame, (lmList[0][1], lmList[0][2]), 15, (0,0,255), cv2.FILLED)
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
        cv2.imshow("pose", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows

if __name__ == "__main__":
    main()