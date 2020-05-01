import cv2
import os
def loadFrame(direc):
	vidcap = cv2.VideoCapture(direc)
	success,image = vidcap.read()
	count = 0
	while success:
		path=os.getcwd()
		cv2.imwrite(path+"/pics/frame%d.jpg" % count, image)     # save frame as JPEG file      
		success,image = vidcap.read()
		#print('Read a new frame: ', success)
		count += 1