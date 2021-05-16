import sys
import cv2
def random_effect(effect_number, img):
	
	if(effect_number == 1):
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		return img_gray
	elif(effect_number == 2):
		img_flip = cv2.flip(img, 0)
		return img_flip
