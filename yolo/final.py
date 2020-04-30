# -*- coding: utf-8 -*-
import os
import cv2    
import numpy as np
import time

def yolo_detect(pathIn='',
                pathOut=None,
                label_path='./cfg/coco.names',
                config_path='./cfg/yolov3_coco.cfg',
                weights_path='./cfg/yolov3_coco.weights',
                confidence_thre=0.5,
                output_prefix = 'test',
                nms_thre=0.3,
                jpg_quality=80):


    LABELS = open(label_path).read().strip().split("\n")
    nclass = len(LABELS)
    
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(nclass, 3), dtype='uint8')
    
    base_path = os.path.basename(pathIn)
    img = cv2.imread(pathIn)
    (H, W) = img.shape[:2]
    
    #print('从硬盘加载YOLO......')
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()
    
    #print('YOLO模型花费 {:.2f} 秒来预测一张图片'.format(end - start))
    
    boxes = []
    confidences = []
    classIDs = []
    
    for output in layerOutputs:
    	for detection in output:
    		scores = detection[5:]
    		classID = np.argmax(scores)
    		confidence = scores[classID]
    
    		if confidence > confidence_thre:
    			box = detection[0:4] * np.array([W, H, W, H])
    			(centerX, centerY, width, height) = box.astype("int")
    
    			
    			x = int(centerX - (width / 2))
    			y = int(centerY - (height / 2))
    
    			boxes.append([x, y, int(width), int(height)])
    			confidences.append(float(confidence))
    			classIDs.append(classID)
    
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_thre, nms_thre)
    
    if len(idxs) > 0:
    	for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = '{}: {:.3f}'.format(LABELS[classIDs[i]], confidences[i])
            (text_w, text_h), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(img, (x, y-text_h-baseline), (x + text_w, y), color, -1)
            cv2.putText(img, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            return(LABELS[classIDs[i]])
    if pathOut is None:
        cv2.imwrite('with_box_'+base_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
        #return(text)
    else:
        cv2.imwrite(pathOut, img, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
        #return(text)


def video2frames(pathIn='', 
                 pathOut='', 
                 only_output_video_info = False, 
                 extract_time_points = None, 
                 initial_extract_time = 0,
                 end_extract_time = None,
                 extract_time_interval = -1, 
                 output_prefix = "",
                 jpg_quality = 100,
                 isColor = True):

    
    cap = cv2.VideoCapture(pathIn)  
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  
    fps = cap.get(cv2.CAP_PROP_FPS)  
    dur = n_frames/fps  

    if only_output_video_info:
        print('only output the video information (without extract frames)::::::')
        print("Duration of the video: {} seconds".format(dur))
        print("Number of frames: {}".format(n_frames))
        print("Frames per second (FPS): {}".format(fps)) 
    
    ##extract frame by given specific time 
    elif extract_time_points is not None:
        if max(extract_time_points) > dur:   ##check the specific time 
            raise NameError('the max time point is larger than the video duration....')
        try:
            os.mkdir(pathOut)
        except OSError:
            pass
        success = True
        count = 0
        while success and count < len(extract_time_points):
            cap.set(cv2.CAP_PROP_POS_MSEC, (1000*extract_time_points[count])) 
            success,image = cap.read()
            if success:
                if not isColor:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  ##convert into black
                print('Write a new frame: {}, {}th'.format(success, count+1))
                cv2.imwrite(os.path.join(pathOut, "{}{:d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                count = count + 1

    else:
        ##check begin time and end time
        if initial_extract_time > dur:
            raise NameError('initial extract time is larger than the video duration....')
        if end_extract_time is not None:
            if end_extract_time > dur:
                raise NameError('end extract time is larger than the video duration....')
            if initial_extract_time > end_extract_time:
                raise NameError('end extract time is less than the initial extract time....')
        
        ##out put every frame in interval
        if extract_time_interval == -1:
            if initial_extract_time > 0:
                cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time)) 
            try:
                os.mkdir(pathOut)
            except OSError:
                pass
            print('Converting a video into frames......')
            if end_extract_time is not None:
                N = (end_extract_time - initial_extract_time)*fps + 1
                success = True
                count = 0
                while success and count < N:
                    success,image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        print('Write a new frame: {}, {}/{}'.format(success, count+1, n_frames))
                        cv2.imwrite(os.path.join(pathOut, "{}{:d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count =  count + 1
            else:
                success = True
                count = 0
                while success:
                    success,image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        print('Write a new frame: {}, {}/{}'.format(success, count+1, n_frames))
                        cv2.imwrite(os.path.join(pathOut, "{}{:d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count =  count + 1

        ##check wether time interval meet the requirement    
        elif extract_time_interval > 0 and extract_time_interval < 1/fps:
            raise NameError('extract_time_interval is less than the frame time interval....')
        elif extract_time_interval > (n_frames/fps):
            raise NameError('extract_time_interval is larger than the duration of the video....')
        
        ##set time interval to 
        else:
            try:
                os.mkdir(pathOut)
            except OSError:
                pass
            print('Converting a video into frames......')
            if end_extract_time is not None:
                N = (end_extract_time - initial_extract_time)/extract_time_interval + 1
                success = True
                count = 0
                while success and count < N:
                    cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time+count*1000*extract_time_interval)) 
                    success,image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        print('Write a new frame: {}, {}th'.format(success, count+1))
                        cv2.imwrite(os.path.join(pathOut, "{}{:d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count = count + 1
            else:
                success = True
                count = 0
                while success:
                    cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time+count*1000*extract_time_interval)) 
                    success,image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        print('Write a new frame: {}, {}th'.format(success, count+1))
                        cv2.imwrite(os.path.join(pathOut, "{}{:d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count = count + 1

def get_video_duration(filename):
  cap = cv2.VideoCapture(filename)
  if cap.isOpened():
    rate = cap.get(5)
    frame_num =cap.get(7)
    duration = frame_num/rate
    return (duration)
  return -1


def final(pathIn, pathOut):
    result=[]
    labellist={}
    frametime = 0

    if(get_video_duration(pathIn) > 300):
        intervaltime = 20
        video2frames(pathIn, pathOut,
                    initial_extract_time=1,
                    end_extract_time=None,
                    extract_time_interval = intervaltime)

        templist = os.listdir(pathOut)
        templist.sort(key=lambda x:int(x[:-4]))

        for file in os.listdir(pathOut):
            frametime= frametime + intervaltime
            yolopathin='./test_imgs/%s'%file
            yolopathout = './result_imgs/%s'%file
            temp = yolo_detect(yolopathin,yolopathout)
            labellist[frametime]=temp
    
        return(labellist)


    else:
        intervaltime = 1

        video2frames(pathIn, pathOut,
            initial_extract_time=intervaltime,
            end_extract_time=None,
            extract_time_interval = 1)

        templist = os.listdir(pathOut)
        templist.sort(key=lambda x:int(x[:-4]))
        #print(templist)

        for file in templist:
        
            frametime = frametime + intervaltime
            yolopathin='./test_imgs/%s'%file
            #print(yolopathin)
            yolopathout = './result_imgs/%s'%file
            temp = yolo_detect(yolopathin,yolopathout)
            #print(temp)
            labellist[frametime] = temp
            #print(labellist[1])

        return(labellist)

        #for key ,value in labellist.items():
           # print(key,',', value)    
            #print(labellist[str(2)])

#path ='./test_imgs'
pathIn = 'test.mp4'
pathOut = './test_imgs'

test =  final(pathIn, pathOut)

for key ,value in test.items():
    print(key,',', value)    
