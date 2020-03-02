import os
import pandas as pd
import cv2
from colab_code.RiderDetector import RiderDetector
from colab_code.RiderDataset import RiderDataset
from colab_code.RiderConfig import RiderConfig
from colab_code.VideoProcessing import VideoProcessing

from mrcnn.utils import Dataset
from mrcnn.config import Config
from mrcnn.model import MaskRCNN

from PyQt5.QtWidgets import *


class Operator:
    def __init__(self):
        self.model_path = 'D:\\Programming\\mask_rcnn_rider_cfg_0131.h5'
        self.model_path = os.path.normpath(self.model_path)
        self.detector = RiderDetector(self.model_path)
        self.processing = VideoProcessing(self.model_path)

    def drawBoxes(self, image):
        boxes = self.detector.extract_boxes(image)

        for box in boxes:
            box.printBBox()
            image = box.drawBBox(image)
        return image, boxes

    def writeBboxesToCsv(self, db_path, image_db_name, boxes, im_h, im_w):
        print(im_h, im_w)
        i = []
        l = []
        x = []
        y = []
        w = []
        h = []

        for box in boxes:
            width = (box.getX2() - box.getX1())
            height = (box.getY2() - box.getY1())

            x_calculated = box.getX1() + (width // 2)
            y_calculated = box.getY1() + (height // 2)

            # by percent to image shape
            width = width / im_w
            height = height / im_h

            x_calculated = x_calculated / im_w
            y_calculated = y_calculated / im_h

            i.append(image_db_name)
            l.append(box.getClassId())
            x.append(x_calculated)
            y.append(y_calculated)
            w.append(width)
            h.append(height)

        # dictionary of lists
        dict = {'image': i, 'label': l, 'x': x, 'y': y, 'width': w, 'height': h}

        df = pd.DataFrame(dict)

        # saving the dataframe
        df.to_csv(db_path, index=False)

    def train_model(self, img_save_path):
        # prepare train set
        # prepare train set
        print('startTrain')
        train_set = RiderDataset()
        train_set.load_dataset(img_save_path, is_train=True)
        train_set.prepare()
        print('Train: %d' % len(train_set.image_ids))
        # prepare test/val set
        test_set = RiderDataset()
        test_set.load_dataset(img_save_path, is_train=False)
        test_set.prepare()
        print('Test: %d' % len(test_set.image_ids))
        # prepare config
        config = RiderConfig()
        config.display()
        # define the model
        model = MaskRCNN(mode='training', model_dir=img_save_path, config=config)
        # load weights (mscoco) and exclude the output layers
        model.load_weights(self.model_path, by_name=True,
                           exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])
        # train weights (output layers or 'heads')
        model.train(train_set, test_set, learning_rate=config.LEARNING_RATE, epochs=1, layers='heads')

        print('trained')

        # setNewModel
        # self.model_path='./confic'

    def convertPreciseVideo(self, video_path, progressBar, output_x, output_y):
        progressBar.setVisible(True)
        print(output_y,output_x)
        self.processing.process_frames(video_path,output_x, output_y, progress_bar=progressBar )


    def drawBoxVideo(self, video_path, progressBar, output_x, output_y):
        progressBar.setVisible(True)
        self.processing.paint_boxes_into_video(video_path,output_x, output_y, progress_bar=progressBar )


    def getNthFrameFromVideo(self, video_path, frame_number):
        cap = cv2.VideoCapture(video_path)

        # get total number of frames
        totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # check for valid frame number
        if frame_number >= 0 & frame_number <= totalFrames:
            # set frame position
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        ret, frame = cap.read()
        return frame

    def getNumberVideoFrames(self, video_path):
        cap = cv2.VideoCapture(video_path)

        # get total number of frames
        totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        return totalFrames
