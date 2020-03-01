import cv2
from tqdm import tnrange
from colab_code.Cropping import Cropping
from colab_code.RiderDetector import RiderDetector
from colab_code.VideoQuality import VideoQuality
from colab_code.Operate_BBoxes import Operate_BBoxes
from PyQt5.QtWidgets import QApplication
from numpy import median

class VideoProcessing:

    def __init__(self, path_weights):
        self.detector = RiderDetector(path_weights)
        self.cropper = Cropping()
        self.bboxOp = Operate_BBoxes()
        self.videoQuality = VideoQuality()
        self.progress_bar = None
        self.size = None
        self.fps = 0
        self.out = None
        self.video = None
        self.frame_counter=0

    def paint_boxes_into_video(self, video_path: str,ratio_x,ratio_y, progress_bar=None):
        self.process_frames(video_path,ratio_x,ratio_y, False,progress_bar)

    def process_frames(self, video_path: str,ratio_x,ratio_y, crop: bool = True, progress_bar=None):
        self.size=(ratio_y, ratio_x)
        self.progress_bar=progress_bar
        boxes = self.get_boxes_and_smooth(video_path)
        self.process_and_write(video_path, boxes, crop)

    def get_boxes_and_smooth(self, video_path: str) -> list:
        self.init(video_path)
        frames = self.get_frames()
        boxes = []
        while len(frames) > 0:
            next_boxes = self.extract_boxes(frames)
            for box in next_boxes:
                boxes.append(box)

            del frames
            frames = self.get_frames()
	boxes = self.removeJumpsFromBoxList(boxes)
        self.shutdown()	
        return self.videoQuality.smooth_boxes(boxes)

    def process_and_write(self, video_path: str, boxes: list, crop):
        self.init(video_path)
        frames = self.get_frames()
        i = 0

        while len(frames) > 0:
            next_boxes = boxes[i:(i + len(frames) - 1)]
            frames = self.crop_frames(frames, next_boxes) if crop else self.draw_boxes(frames, boxes)
            self.write(frames)
            del frames
            frames = self.get_frames()
            i += len(frames)

        self.shutdown()

    def downscale_frame(self, frame, scale):
        return cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    def extract_boxes(self, frames) -> list:
        downscale_factor = 0.5
        upscale_factor = 1.0 / downscale_factor
        boxes = []

        for i in range(0, len(frames)):
            if self.progress_bar is not None:
                self.frame_counter +=1
                self.progress_bar.setValue(self.frame_counter)
                QApplication.processEvents()

            downsize_img = self.downscale_frame(frames[i], downscale_factor)
            boxes.append(self.detector.getBox(downsize_img))
        self.bboxOp.scale_bboxes_list(boxes, upscale_factor)

        return boxes

    def crop_frames(self, frames, boxes):
        cropped_frames = []

        for i in range(0, len(boxes)):
            cropped_frames.append(self.cropper.crop_image(boxes[i], frames[i]))

        return cropped_frames

    def draw_boxes(self, frames, boxes):
        frames_with_boxes = []

        for i in range(0, len(boxes)):
            frames_with_boxes.append(boxes[i].drawBBox(frames[i]))

        return frames_with_boxes

    # Checks previous boxes and removes current box if too far away
    def removeJumpsFromBoxList(self, boxes):
        numOfLastBoxes = 25     # Number of last boxes who are checked with median
        allowedDistance = 300    # Max Distance allowed
        allowedBoxesToReset = 75 # When to interrupt

        numOfResetBoxes = 0
        
        for index, box in enumerate(boxes):
          lastBoxes = []
          
          if index-numOfLastBoxes >= 0:
            lastNBoxes = boxes[index-numOfLastBoxes:index]
            lastNBoxesX = list()
            lastNBoxesY = list()

            # Add all X/Y Values to their lists
            for Box in lastNBoxes:  
              lastNBoxesX.append(self.calcMiddlepoint(Box.getX1(), Box.getX2()))
              lastNBoxesY.append(self.calcMiddlepoint(Box.getY1(), Box.getY2()))
            boxCenterX = self.calcMiddlepoint(box.getX1(), box.getX2())
            boxCenterY = self.calcMiddlepoint(box.getY1(), box.getY2())
            medianX = median(lastNBoxesX)
            medianY = median(lastNBoxesY)
            distance = (((boxCenterX - medianX) ** 2) + ((boxCenterY - medianY) ** 2)) ** 0.5

            # If too far away ignore this box
            if distance > allowedDistance:
              # Check if its allowed to replace more boxes otherwise reset
              if numOfResetBoxes <= allowedBoxesToReset:
                boxes[index] = boxes[index-1]
                numOfResetBoxes += 1 
              else:
                numOfResetBoxes = 0
            else:
              numOfResetBoxes = 0
        
        return boxes

    # Calcs the value inbetween two 1d Values
    def calcMiddlepoint(self, x, y):
        result = (x-y)/2 + x
        return result

    def write(self, frames: list):
        for img in frames:
            self.out.write(cv2.resize(img, self.size))

    def get_frames(self):
        success, img = self.video.read()
        frames = []
        number = 10

        while success and (number > 0):
            frames.append(img)
            success, img = self.video.read()
            number = number - 1
        del img

        return frames

    def init(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_counter = 0
        print('Number of frames:',length)
        if self.progress_bar is not None:
            self.progress_bar.setMaximum(length)
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
        self.out = self.get_out_object()

    def get_out_object(self):
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        filename = 'result.mp4'
        return cv2.VideoWriter(filename, fourcc, self.fps, self.size)

    def shutdown(self):
        self.video.release()
        self.out.release()
