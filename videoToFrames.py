# this is a small example how to read the labels for the rimondo dataset using pandas
# and identifying the corresponding rectangles
# author: soeren.klemm@uni-muenster.de
# date: 19. Nov. 2019
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

from os.path import join

import cv2

from PIL import Image
from PIL import ImageDraw
import moviepy.editor as mpe

# Setting up Database
DATABASE = "rimondo_filtered.csv"
label_data = pd.read_csv(DATABASE)

# colors used for drawing rectangles 1: Horse, 2: Rider
colors = {1: (0,0,255), 2: (0,255,0)}


# create Video from Frames
# Input: frame_source: Folder with .png frames,
#        fps: Fps of the created video
# Output: Video in .avi format
def createVideo(frame_source, fps):
    # sort frames in path --> must be named sufficently
    frames = sorted([fname for fname in os.listdir(frame_source) if fname.endswith('.png')],
                    key=lambda f: int(f.rsplit(os.path.extsep, 1)[0].rsplit(None, 1)[-1]))
    print(len(frames))
    if (len(frames) > 0):
        img = cv2.imread(join(frame_source, frames[0]))
        size = (img.shape[1], img.shape[0])
        # Create Videofile
        out = cv2.VideoWriter(os.path.basename(frame_source)+'.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        # For every frame in the folder. Add frame to video
        for frame in frames:
            print(frame)
            image_file = join(frame_source, frame)
            img = cv2.imread(image_file)
            out.write(img)
            del img
        out.release()


# creates Frames from a Video
# Input: video_path: Path to the video
# Output: Returns the FPS of the video
def createFrames(video_path):
    # Path to video file
    video = cv2.VideoCapture(video_path)

    count = 1                      # Used as counter variable
    success = 1                 # checks whether frames were extracted
    fps = video.get(cv2.CAP_PROP_FPS)

    while success:

        # function extract frames
        success, image = video.read()

        # Found Image
        if success:
            # Saves the frames with frame-count
            # cv2.imwrite("../../framesTest/%d.png" % count, image)

            # If wanted: Create Folder and save frame
            # folderPath = video_path.strip('.avi')

            height = image.shape[0]     # Get height/width from picture
            width = image.shape[1]

            # Getting Data from Database

            videoid = video_path.strip(".avi") # Name of the Video / Used know where to search in Database
            """
            RectangleData = getPictureDataFromDatabase(count, videoid, height, width)
            for Rect in RectangleData:
                if Rect[0] != (0,0):
                    image = cv2.rectangle(image, Rect[0], Rect[1], colors[Rect[2]], 3)
            """
            print(count)
            # Save Image to folder
            cv2.imwrite(os.path.dirname(os.path.abspath(__file__)) + "/framesTest/"+ videoid + "/%d.png" % count, image)
            count += 1

        del image

    return fps

# Input: An imageName, VideoID FolderName where this image can be found
# Output: List of all Rectangle Datas for this picture
def getPictureDataFromDatabase(imageID, VideoID, height, width):
    imageID += 17
    csvID = VideoID + "/" + str(imageID).zfill(5) + ".jpg"
    RectangleData = []
    #print(imageID,VideoID,height,width)
    #print("CSVID: ",csvID)

    for item in [1, 2]:
        # select rows for the given image and current item (horse or rider)
        all_rects = label_data.loc[
            (label_data["image"] == csvID) & (label_data["label"] == item)
            ]
        for _, entry in all_rects.iterrows():
            # x and y define the center of the bounding box
            # all values are relative to image height/width
            x = entry["x"] * width
            y = entry["y"] * height
            w = entry["width"] * width
            h = entry["height"] * height

            x1 = x - w // 2
            y1 = y - h // 2
            x2 = x + w // 2
            y2 = y + h // 2
            rectangle = ((int(x1), int(y1)), (int(x2), int(y2)), item)
            RectangleData.append(rectangle)

    return RectangleData


# Reads all Images of a video, edits pics and saves it as a video
# Input: video_path: Path to a MP4 Video

def cropVideo(video_path):
    # Path to video file
    video = cv2.VideoCapture(video_path)
    filename = os.path.basename(video_path)
    count = 0  # Frame counter
    fps = video.get(cv2.CAP_PROP_FPS)

    # Check for first picture
    success, img = video.read()

    if (success):
        #size = (img.shape[1], img.shape[0])
        size = (1920, 1080)
        print(size)
    else:
        print("No Picture found")
        raise ValueError

    # VideoData
    print("NAME: "+filename.strip('.mp4')+'Crop.mp4')
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(filename.strip('.mp4')+'Crop.mp4', fourcc, fps, size)

    while True:
        print(count)
        if (success):
            x = 50
            y = 50
            w = 500
            h = 500
            img = img[y:y+h, x:x+w]
            #cv2.imshow("Image", imcrop)
            img = cv2.resize(img, size)
            out.write(img)
        else:
            print("failed")
            break
        del img
        count += 1
        success, img = video.read()

    out.release()

    videoclip = mpe.VideoFileClip(filename.strip('.mp4')+'Crop.mp4')

    #Audiostuff, takes alot longer tho
    #audioclip = mpe.CompositeAudioClip([mpe.AudioFileClip(video_path)])
    #videoclip.audio = audioclip
    #videoclip.write_videofile(filename.strip('.mp4')+'Crop2.mp4')


def main():
    #createFrames("GOPR8291.avi")
    #createVideo(os.path.dirname(os.path.abspath(__file__))+"/frames/GOPR8291", 4)

    #cropVideo("Video1.mp4")

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    cropVideo(file_path)

if __name__ == '__main__':
    main()
