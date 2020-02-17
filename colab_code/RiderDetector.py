# Detection of rider by bounding boxes
import cv2
from mrcnn.model import MaskRCNN
from colab_code.RiderConfig import RiderConfig
from colab_code.Cropping import Cropping


class RiderDetector:

    def __init__(self, path_weights):
        self.model = self.setModel(path_weights)
        self.target_descriptor = None
        self.target_box = None
        self.cropper = Cropping()

    def setModel(self, path_weights):
        config = RiderConfig()
        # define the model
        model = MaskRCNN(mode='inference', model_dir='./', config=config)
        # load trained weights
        model.load_weights(path_weights, by_name=True)
        return model

    def getBox(self, image):
        """ Get Box for one image
        Gibt letzte Box zurück, wenn er keine findet.
        @:raises Exception"""
        boxes = self.extract_boxes(image)
        pair_boxes = self.get_rider_pairs(boxes, image)

        if len(pair_boxes) == 0:
            return {"id": 1, "x1": 100, "x2": 200, "y1": 100, "y2": 200}

        pair_box = pair_boxes.pop(0)

        if self.target_descriptor is None:
            self.target_descriptor = self.get_descriptor(image, pair_box)
            self.target_box = pair_box
        else:
            pass
            # return self.find_target(image, pair_boxes)
        return pair_box

    def box_to_dict(self, box, class_id):
        return {"id": class_id, "x1": box[1], "x2": box[3], "y1": box[0], "y2": box[2]}

    def upscale_bbox(self, bbox, scale):
        x1 = bbox["x1"] * scale
        x2 = bbox["x2"] * scale
        y1 = bbox["y1"] * scale
        y2 = bbox["y2"] * scale
        class_id = bbox["id"]
        b = {"id": class_id, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
        return b

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

    def get_descriptor(self, image, box):
        cropped = self.cropper.crop_image(box, image)
        _, descriptor = cv2.ORB().detectAndCompute(cropped, None)

        return descriptor

    def get_rider_pairs(self, boxes: list, image) -> list:
        pairs = []
        n = len(boxes)
        for i in range(0, n):
            for j in range(i + 1, n):
                bi = boxes[i]
                bj = boxes[j]
                if self.do_overlap(bi, bj) and self.is_pair(bi, bj):
                    pairs.append(self.cropper.complete_bbox(image, [bi, bj]))
        return pairs

    def calculate_score(self, descriptor):
        matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

        return len(matcher.match(self.target_descriptor, descriptor))

    def find_target(self, image, boxes: list):
        found = boxes[0]
        score = self.calculate_score(self.get_descriptor(image, found))

        for box in boxes:
            descriptor = self.get_descriptor(image, box)
            new_score = self.calculate_score(descriptor)
            if new_score > score:
                found = self.get_descriptor(image, box)
        return found

    def do_overlap(self, box1, box2):
        width = self.calc_intersection(box1['x1'], box1['x2'], box2['x1'], box2['x2'])
        height = self.calc_intersection(box1['y1'], box1['y2'], box2['y1'], box2['y2'])

        return (width * height) > 0

    def calc_intersection(self, a0, a1, b0, b1):
        if a0 >= b0 and a1 <= b1:  # Contained
            intersection = a1 - a0
        elif a0 < b0 and a1 > b1:  # Contains
            intersection = b1 - b0
        elif a0 < b0 < a1:  # Intersects right
            intersection = a1 - b0
        elif a1 > b1 > a0:  # Intersects left
            intersection = b1 - a0
        else:  # No intersection (either side)
            intersection = 0

        return intersection

    def extract_boxes(self, image):
        results = self.model.detect([image], verbose=0)
        r = results[0]
        rois = r['rois']
        class_ids = r['class_ids']

        boxes = []
        for i in range(0, len(class_ids)):
            box = self.box_to_dict(rois[i], class_ids[i])
            boxes.append(box)

        return boxes

    def is_pair(self, box1, box2):
        return (box1['id'] + box2['id']) == 3
