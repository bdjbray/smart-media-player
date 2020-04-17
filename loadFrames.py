import cv2
def loadFrame(direc):
	vidcap = cv2.VideoCapture(direc)
	success,image = vidcap.read()
	count = 0
	while success:
  		cv2.imwrite("/Users/brayb/Downloads/pythonws/ec500/homework5_6/smart_media_player/pics/frame%d.jpg" % count, image)     # save frame as JPEG file      
  		success,image = vidcap.read()
  		#print('Read a new frame: ', success)
  		count += 1