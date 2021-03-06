# -*- coding: utf-8 -*-
import os
import cv2    
import numpy as np
import time




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
        return count

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
        num=video2frames(pathIn, pathOut,
                    initial_extract_time=1,
                    end_extract_time=None,
                    extract_time_interval = intervaltime)

        templist = os.listdir(pathOut)
        templist.sort(key=lambda x:int(x[:-4]))

        for file in os.listdir(pathOut):
            frametime= frametime + intervaltime
            yolopathin='./test_imgs/%s'%file
            yolopathout = './result_imgs/%s'%file
            #temp = yolo_detect(yolopathin,yolopathout)
            #labellist[frametime]=temp
    
        return num


    else:
        intervaltime = 1

        num=video2frames(pathIn, pathOut,
            initial_extract_time=intervaltime,
            end_extract_time=None,
            extract_time_interval = 1)

        templist = os.listdir(pathOut)
        templist.sort(key=lambda x:int(x[:-4]))
        print(templist)

        for file in templist:
        
            frametime = frametime + intervaltime
            yolopathin='./test_imgs/%s'%file
            #print(yolopathin)
            yolopathout = './result_imgs/%s'%file
            #temp = yolo_detect(yolopathin,yolopathout)
            #print(temp)
            #labellist[frametime] = temp
            #print(labellist[1])

        return num
