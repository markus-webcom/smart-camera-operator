import os
import pandas as pd
from os.path import join
import cv2
from mrcnn.utils import Dataset
from numpy import zeros
from numpy import asarray
import math


# class that defines and loads the dataset for train and test
class RiderDataset(Dataset):

    def getClassname(self, index):
        class_names = ['BG', 'horse', 'rider']
        if 0 <= index < 3:
            return class_names[index]
        else:
            return -1

    def load_dataset(self,image_dir, is_train=True):
        # define classes
        self.add_class("dataset", 1, "horse")
        self.add_class("dataset", 2, "rider")

        FRAME_SOURCE = image_dir
        # where to find the labels
        db = join(image_dir,'annotations')

        frames = [f for f in os.listdir(image_dir) if f.endswith(".png") or f.endswith('.jpg')]
        numberDataset = len(frames)
        borderTest = round(numberDataset * 0.9)

        for i in range(numberDataset):
                image_path = join(FRAME_SOURCE,frames[i])
                # skip all test images if we are building the train set
                if not is_train and i < borderTest:
                    continue
                # skip all train images if we are building the test/val set
                if is_train and i >= borderTest:
                    continue
                # add to dataset
                self.add_image('dataset', image_id=i, path=image_path, annotation=db)

    def extract_boxes(self, img_path):
        dir_name=os.path.dirname(img_path)
        img_name=os.path.splitext(os.path.basename(img_path))[0]
        db_path=join(dir_name,'annotations')
        db_path=join(db_path,img_name+'.csv')

        allEntries = pd.read_csv(db_path)

        img = cv2.imread(img_path)
        height = img.shape[0]
        width = img.shape[1]
        bbox = []
        for _, entry in allEntries.iterrows():

            x = entry["x"] * width
            y = entry["y"] * height
            w = entry["width"] * width
            h = entry["height"] * height
            # Eckpunkte bbox berechnen
            xmin = round(x - w // 2)
            xmax = round(x + w // 2)
            ymin = round(y - h // 2)
            ymax = round(y + h // 2)
            if entry["label"] == 1 or entry["label"] == 2:
                box = [entry["label"], xmin, ymin, xmax, ymax]
                bbox.append(box)
        return bbox, height, width

    # load the masks for an image
    def load_mask(self, image_id):
        # get details of image
        info = self.image_info[image_id]
        # define box file location
        db_path = info['annotation']
        img_path = info['path']

        # load boxes
        boxes, h, w = self.extract_boxes(img_path)
        # create one array for all masks, each on a different channel
        masks = zeros([h, w, len(boxes)], dtype='uint8')
        # create masks
        class_ids = list()
        for i in range(len(boxes)):
            box = boxes[i]
            row_s, row_e = box[2], box[4]
            col_s, col_e = box[1], box[3]
            masks[row_s:row_e, col_s:col_e, i] = 1

            if box[0] == 1:
                class_ids.append(self.class_names.index('horse'))
            if box[0] == 2:
                class_ids.append(self.class_names.index('rider'))
        return masks, asarray(class_ids, dtype='int32')

    # load an image reference
    def image_reference(self, image_id):
        info = self.image_info[image_id]
        return info['path']
