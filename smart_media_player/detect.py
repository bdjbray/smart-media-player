import cv2
import cvlib as cv

def detect():
	img = cv2.imread("/Users/brayb/Downloads/pythonws/ec500/homework5_6/smart_media_player/pics/frame5.jpg")
	boxes, labels, _conf = cv.detect_common_objects(img, model="yolov3")

	print(labels)
	return labels

