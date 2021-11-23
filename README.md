# DriveAtHome
***
This is my Graduate Project on my college.  
I didn't sort out files yet, plz wait a second, I will come back soon!  
This version is not complete, because some private factor, we can't upload all of the img and video resource, so sorry about that.  
And the detail about our car will be upload soon as well, thank you for your waiting.  

## how to play?
### how to execute...
We use Openpose from Mediapipe to check the body points of people, and calculate it to make people drive the arduino car.  
You can run the Connecttest02.py file to execute this project, if you can't I think is beacause lack of some resource, we're so sorry about that, maybe you can find some substitutions or alternatives.  

### AR
AR is reference from [here](https://github.com/jayantjain100/Augmented-Reality)!!! Thanks a lot!   
We use aruco markers and put the 3D model on it, player can drive our arduino car and based on the image return from the car to recognize markers, if recognize successfully the 3D model will overlap on the marker.  
And we will check the success image, if the area of marker is bigger than one specific value, we will consider that it's collision.  
If collide correctly, we will overlay an effect after collision, you can check image below.  
![image](https://user-images.githubusercontent.com/79491377/143031157-723de0ec-5185-41c5-b1ad-701dafb36d34.png)


### Openpose
The driving pose we're reference from [here](https://github.com/fabian57fabian/OpenPose-to-robotics), we use the same way to control our auduino car.  
The second way to control our car is based on the body points, you can check it below.  
![bodypose 1](https://user-images.githubusercontent.com/79491377/135737599-40c7a1e8-b659-4ddd-8bc2-2b4164114771.gif)

## video link
Our second milestone video link is below, check it out!  
[second milestone](https://www.youtube.com/watch?v=LEmxmKcIMYo)


---
## reference
The AR resource is reference from [here](https://github.com/jayantjain100/Augmented-Reality), it's so amazing, I learn a lot!

Openpose we're using [Mediapipe](https://mediapipe.dev/), it's so convienient for laptop user.

And the arduino car we're reference from [here](https://github.com/fabian57fabian/OpenPose-to-robotics), thanks a lot!  
