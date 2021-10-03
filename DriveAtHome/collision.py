import sys
from typing import KeysView
import cv2
import numpy as np

def random_effect(effect_number, img):
	if(effect_number == 1):
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		return img_gray
	elif(effect_number == 2):
		img_flip = cv2.flip(img, 0)
		return img_flip
	elif(effect_number == 3):
		img_copy = img.copy()
		gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray_frame = np.float32(gray_frame)
		dst = cv2.cornerHarris(gray_frame, blockSize = 6, ksize = 5, k = 0.04)
		img_copy[dst > 0.05 * dst.max()] = [0,255,0]
		return img_copy
	elif(effect_number == 4):
		blur = cv2.blur(img,(20,20))
		return blur