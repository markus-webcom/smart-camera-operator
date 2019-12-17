import os
import pandas as pd
from PyQt5.QtWidgets import QFileDialog
from os.path import join
import cv2
import moviepy.editor as mpe
import training_rider
from PyQt5.QtWidgets import QProgressBar

class VideoToFrames:

    model = training_rider.setModel("C:\\Users\\Tobia\\Desktop\\smart-camera-operator-develop\\mask_rcnn_rider_cfg_0005.h5")
    def __init__(self):
        #print(os.path.dirname(os.path.abspath('mask_rcnn_rider_cfg_0001.h5')))
        #model =
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
        print(filename)
        if success:
            # size = (img.shape[1], img.shape[0])
            print("imshp0: ", img.shape[0])
            print("imshp1: ",  img.shape[1])
            sizeX = 1280  # HD
            sizeY = 720
            size = (sizeX, sizeY)
            ratio = sizeX / sizeY
        else:
            print("No Picture found")
            raise ValueError

        # VideoData
        print("NAME: " + filename.strip('.MP4') + 'Crop.mp4')
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(filename.strip('.MP4') + 'Crop.mp4', fourcc, fps, size)

        while True:
            progress_bar.setValue((count / total_frames) * 100)
            if success:
                print(count)
                bbox = training_rider.getBboxes(img, self.model)
                print(bbox)
                X1arr = []
                Y1arr = []
                X2arr = []
                Y2arr = []
                print("test1")
                for i in bbox:
                    X1arr.append(i["x1"])
                    Y1arr.append(i["y1"])
                    X2arr.append(i["x2"])
                    Y2arr.append(i["y2"])
                print("test2")
				# bessere Loesung statt ueberspringen von Frames waere schoen
				if(len(X1arr)==0):
                  print(bbox)
                  del img
                  count += 1
                  success, img = video.read()
                  continue
                X1 = min(X1arr)
                Y1 = min(Y1arr)
                X2 = max(X2arr)
                Y2 = max(Y2arr)
                print("test3")
                print(X1,Y1,X2,Y2)

                if count == 21:
                    print("test")
                TotalYPixels = Y2 - Y1  # Total amount of pixels of the bounding box in Y direction
                if TotalYPixels < 480: TotalYPixels = 480
                TotalXPixels = TotalYPixels * ratio  # Total amount of pixel of the bounding box in X direction

                # Out of Bounds check if bounding box gets bigger than img size
                if TotalYPixels > img.shape[0]: TotalYPixels = img.shape[0]
                if TotalXPixels > img.shape[1]: TotalXPixels = img.shape[1]

                # Calculate optimal Crop points to maintain ratio
                CropX1 = (X2 + X1) / 2 - TotalXPixels / 2  # Defines the left most pos to crop the pic
                CropX2 = (X2 + X1) / 2 + TotalXPixels / 2  # Defines the right most pos to crop the pic
                CropY1 = (Y2 + Y1) / 2 - TotalYPixels / 2  # Defines the top most pos to crop the pic
                CropY2 = (Y2 + Y1) / 2 + TotalYPixels / 2  # Defines the bottom most pos to crop the pic

                # Out of Bounds check
                if CropX1 < 0:  # If we are out of bounds to the left side, adjust both X pos to the right
                    CropX2 += -1 * CropX1
                    CropX1 = 0

                if CropX2 > img.shape[1]:  # If we are out of bounds to the right side, adjust both X pos to the left
                    CropX1 += (img.shape[1] - CropX2)
                    CropX2 = img.shape[1]

                if CropY1 < 0:  # If we are out of bounds to the upper side, adjust both Y pos down
                    CropY2 += -1 * CropY1
                    CropY1 = 0

                if CropY2 > img.shape[0]:  # If we are out of bounds to the lower side, adjust both Y pos up
                    CropY1 += (img.shape[0] - CropY2)
                    CropY2 = img.shape[0]

                # Don't Crop when where are no Rectangles
				CropX1=int(CropX1)
                CropX2=int(CropX2)
                CropY1=int(CropY1)
                CropY2=int(CropY2)
                if X1 != img.shape[1] and Y1 != img.shape[0]:
                    img = img[CropY1:CropY2,CropX1:CropX2]
                    # cv2.imshow("Image", imcrop)
                    img = cv2.resize(img, size)
                    out.write(img)

            # total_frames
            if count >= total_frames: #Abort when framelimit is reached
                break
                print("Done")
            del img
            count += 1
            success, img = video.read()

        out.release()
        videoclip = mpe.VideoFileClip(filename.strip('.MP4') + 'Crop.mp4')
        # Audiostuff, takes alot longer tho
        # audioclip = mpe.CompositeAudioClip([mpe.AudioFileClip(video_path)])
        # videoclip.audio = audioclip
        # videoclip.write_videofile(filename.strip('.mp4')+'Crop2.mp4')