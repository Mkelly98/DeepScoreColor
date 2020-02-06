import cv2
import os
import sys

mypath = os.getcwd()
filename = input("filename: ")
title = filename[0:(len(filename)-4)] # removes .mp4 from clip
try:
    if not os.path.exists(mypath + "/" + title + "Frames"):
        os.makedirs(mypath + "/" + title + "Frames")
except OSError:
    print('Error: Creating directory of data')
vidcap = cv2.VideoCapture(mypath + "/" + filename)

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(mypath + "/" + title + "Frames/frame" + str(sec)+ " sec.jpg", image)    # save frame as JPG file
    return hasFrames

sec = 0
frameRate = 0.5 #it will capture image in each 0.5 second
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

    # try:
    #     if not os.path.exists('/Users/aniajordan/Dev/Frames/data'):
    #         os.makedirs('/Users/aniajordan/Dev/Frames/data')
    # except OSError:
    #     print('Error: Creating directory of data')
    # vidcap = cv2.VideoCapture('/Users/aniajordan/Dev/Frames/budapest.mp4')
    # def getFrame(sec):
    #     vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    #     hasFrames,image = vidcap.read()
    #     if hasFrames:
    #         cv2.imwrite("/Users/aniajordan/Dev/Frames/data/frame "+str(sec)+" sec.jpg", image)     # save frame as JPG file
    #     return hasFrames
    # sec = 0
    # frameRate = 0.5 #it will capture image in each 0.5 second
    # success = getFrame(sec)
    # while success:
    #     sec = sec + frameRate
    #     sec = round(sec, 2)
    #     success = getFrame(sec)
