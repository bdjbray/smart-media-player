import cv2
import cvlib as cv
import os

def detect(theframe):
	path=os.getcwd()
	img = cv2.imread(path+"/pic2/"+str(theframe)+".jpg")
	boxes, labels, _conf = cv.detect_common_objects(img, model="yolov3")

	print(labels)
	return labels

