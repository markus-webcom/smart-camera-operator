# this is a small example how to read the labels for the rimondo dataset using pandas
# and identifying the corresponding rectangles
# author: soeren.klemm@uni-muenster.de
# date: 19. Nov. 2019
import os
import pandas as pd

from os.path import join
import cv2

import moviepy.editor as mpe



# create Video from Frames
def createVideo(frame_source,fps):

    # sort frames in path --> must be named sufficently
    frames = sorted([fname for fname in os.listdir(frame_source) if fname.endswith('.png')],
                    key=lambda f: int(f.rsplit(os.path.extsep, 1)[0].rsplit(None, 1)[-1]))
    print(len(frames))
    if(len(frames)>0):
        img = cv2.imread(join(frame_source, frames[0]))
        size = (img.shape[1], img.shape[0])
        out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        for frame in frames:
            print(frame)
            image_file = join(frame_source, frame)
            img=cv2.imread(image_file)
            out.write(img)
            del img
        out.release()


# create Frames from Video
def createFrames(video_path):
    # Path to video file
    video = cv2.VideoCapture(video_path)
    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1
    fps = video.get(cv2.CAP_PROP_FPS)
    while success:

        # vidObj object calls read
        # function extract frames
        success, image = video.read()
        if(success):
            # Saves the frames with frame-count
            cv2.imwrite("../../framesTest/%d.png" % count, image)
            print(count)
        del image

        count += 1
    return fps

# kein Zwischenspeichern von frames
# counter kann gelöscht werden
def cropVideo(video_path):
    # Path to video file
    video = cv2.VideoCapture(video_path)

    # Used as counter variable
    count = 0

    fps = video.get(cv2.CAP_PROP_FPS)

    success, img = video.read()

    if (success):
        size = (img.shape[1], img.shape[0])
    else:
        print("error")
        raise ValueError
    fourcc =  cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter('project.mp4', fourcc , fps, size)
    while True:

        print(count)
        if (success):
            # crop picture here
            out.write(img)
        else:
            print("failed")
            break
        del img
        count += 1
        success, img = video.read()

    out.release()
    print("start audio")

    videoclip = mpe.VideoFileClip('project.mp4')
    audioclip = mpe.AudioFileClip(video_path)

    new_audioclip = mpe.CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile("project2.mp4")





def main():

    # fps=createFrames("../../videos/GP028291.mp4")
    # createVideo("../../framesTest", fps)
    cropVideo("../../videos/nature.mp4")

if __name__ == '__main__':
    main()