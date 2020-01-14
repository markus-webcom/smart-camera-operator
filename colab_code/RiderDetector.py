# Detection of rider by bounding boxes
import cv2
from mrcnn.model import MaskRCNN
from colab_code.RiderConfig import RiderConfig


class RiderDetector:

    def __init__(self, path_weights):
        self.model = self.setModel(path_weights)

    def setModel(self, path_weights):
        config = RiderConfig()
        # define the model
        model = MaskRCNN(mode='inference', model_dir='./', config=config)
        # load trained weights
        model.load_weights(path_weights, by_name=True)
        return model

    # get bounding boxes for one image
    def getBboxes(self, im):
        results = self.model.detect([im], verbose=0)
        r = results[0]
        # extract ids and bboxes for riders
        rois = r['rois']

        bbox = []
        counter = -1
        for i in r['class_ids']:
            counter = counter + 1
            b = self.box_to_dict(rois[counter], i)
            bbox.append(b)
        # austauschen mit crop methode statt zeichnen
        # drawBox(imagepath, bbox)
        return bbox

    # get bounding boxes for list of frames
    def getBboxes_framelist(self, frames):
        bbox_list = list()
        for i in range(len(frames)):
            bbox_list.append(self.getBboxes(frames[i]))
        return bbox_list

    def box_to_dict(self, box, class_id):
        b = {"id": class_id, "x1": box[1], "x2": box[3], "y1": box[0], "y2": box[2]}
        return b

    def upscale_bbox(self, bbox, scale):
        x1 = bbox["x1"] * scale
        x2 = bbox["x2"] * scale
        y1 = bbox["y1"] * scale
        y2 = bbox["y2"] * scale
        class_id = bbox["id"]
        b = {"id": class_id, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
        return b

    def upscale_all_bboxes(self, bbox_list, scale):
        upscaled_bboxes = list()
        for i in range(len(bbox_list)):
            boxes = list()
            for j in bbox_list[i]:
                boxes.append(self.upscale_bbox(j, scale))
            upscaled_bboxes.append(boxes)
            del boxes
        return upscaled_bboxes

    def upscale_bboxes_list(self, bbox_list, scale):
        upscaled_bboxes = list()
        for i in bbox_list:
            upscaled_bboxes.append(self.upscale_bbox(i, scale))
        return upscaled_bboxes

    # only for debugging
    def drawBox(self, image, box):
        # cv2 colors are in BGR instead of RGB
        colors = {0: (0, 255, 2550), 1: (0, 0, 255), 2: (255, 255, 0), 3: (255, 0, 0)}
        y1 = int(box['y1'])
        x1 = int(box['x1'])
        y2 = int(box['y2'])
        x2 = int(box['x2'])
        class_id = int(box['id'])

        image = cv2.rectangle(image, (x1, y1), (x2, y2), colors[class_id], 2)

        return image


