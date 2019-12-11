import os
import pandas as pd
from PyQt5.QtWidgets import QFileDialog
from os.path import join
import cv2
import moviepy.editor as mpe
from PyQt5.QtWidgets import QProgressBar


class VideoToFrames:

    def __init__(self):
        pass

    def crop(self, video_path: str, progress_bar: QProgressBar):
        # createFrames("GOPR8291.avi")
        # createVideo(os.path.dirname(os.path.abspath(__file__))+"/frames/GOPR8291", 4)
        # cropVideo("Video1.mp4")
        # Path to video file
        video = cv2.VideoCapture(video_path)
        filename = os.path.basename(video_path)
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        count = 0  # Frame counter
        fps = video.get(cv2.CAP_PROP_FPS)

        # Check for first picture
        success, img = video.read()

        if success:
            # size = (img.shape[1], img.shape[0])
            size = (1920, 1080)
            print(size)
        else:
            print("No Picture found")
            raise ValueError

        # VideoData
        print("NAME: " + filename.strip('.mp4') + 'Crop.mp4')
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(filename.strip('.mp4') + 'Crop.mp4', fourcc, fps, size)

        while True:
            progress_bar.setValue((count / total_frames) * 100)
            if success:
                x = 50
                y = 50
                w = 500
                h = 500
                img = img[y:y + h, x:x + w]
                # cv2.imshow("Image", imcrop)
                img = cv2.resize(img, size)
                out.write(img)
            else:
                break
            del img
            count += 1
            success, img = video.read()

        out.release()
        videoclip = mpe.VideoFileClip(filename.strip('.mp4') + 'Crop.mp4')
        # Audiostuff, takes alot longer tho
        # audioclip = mpe.CompositeAudioClip([mpe.AudioFileClip(video_path)])
        # videoclip.audio = audioclip
        # videoclip.write_videofile(filename.strip('.mp4')+'Crop2.mp4')
