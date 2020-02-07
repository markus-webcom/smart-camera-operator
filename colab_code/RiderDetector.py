# Detection of rider by bounding boxes
import cv2
import numpy as np
from mrcnn.model import MaskRCNN
from colab_code.RiderConfig import RiderConfig
from colab_code.BoundingBox import BoundingBox

class RiderDetector:

    def __init__(self, path_weights):
        self.model = self.setModel(path_weights)

        # set model for detection

    def setModel(self, path_weights):
        config = RiderConfig()
        # define the model
        model = MaskRCNN(mode='inference', model_dir='./', config=config)
        # load trained weights
        model.load_weights(path_weights, by_name=True)
        return model

        # get bounding boxes for one image

    def detect_boxes(self, im):
        results = self.model.detect([im], verbose=0)
        r = results[0]
        # extract ids and bboxes for riders
        rois = r['rois']

        bbox = []
        counter = -1
        for i in r['class_ids']:
            counter = counter + 1
            b = self.detected_box_to_BBox(rois[counter], i)
            bbox.append(b)
        return bbox

        # get bounding boxes for list of frames

    def getBboxes_framelist(self, frames):
        bbox_list = list()
        for i in range(len(frames)):
            bbox_list.append(self.detect_boxes(frames[i]))
        return bbox_list

        # detection bounding box to dict

    def detected_box_to_BBox(self, box, class_id):
        return BoundingBox(box[1],box[3],box[0],box[2],class_id)




