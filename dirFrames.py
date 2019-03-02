import cv2
import os
import sys
name =input("directory: ")
title = input("Title: ") # what do you want to name the file
fh = "/{0}Frames/".format(title)
currDir = os.getcwd() # gets current directory
mypath = currDir + "/" + name; # gets name of dir you want
for root, dirs, files in os.walk(mypath):
    for filename in files:
        title = filename[0:(len(filename)-4)] # removes .mp4 from clip
        try:
            if not os.path.exists(currDir + fh):
                os.makedirs(currDir + fh) # makes main frame dir
        except OSError:
            print('Error: Creating directory of frames')
        try:
            if not os.path.exists(currDir + fh + title ): # makes dir for this clip's frames
                os.makedirs(currDir + fh + title)
        except OSError:
            print('Error: Creating directory of frames inner folders')
        vidcap = cv2.VideoCapture(mypath + "/" + filename) # manipulates current clip
        #
        def getFrame(sec):
            vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
            hasFrames,image = vidcap.read()
            if hasFrames:
                cv2.imwrite(currDir + fh + title + "/frame" + str(sec)+ " sec.jpg", image)    # save frame as JPG file
            return hasFrames

        sec = 0
        frameRate = 2.5 #it will capture image in each 0.5 second
        initialSuccess = getFrame(sec)
        success = initialSuccess
        while success:
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(sec)
if initialSuccess:
    print("Frame conversion completed")
else:
    print("Frame conversion incomplete")
