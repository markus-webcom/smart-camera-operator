# Detection of rider by bounding boxes
import cv2
from mrcnn.model import MaskRCNN
from colab_code.RiderConfig import RiderConfig


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
            b = self.box_to_dict(rois[counter], i)
            bbox.append(b)
        # austauschen mit crop methode statt zeichnen
        # drawBox(imagepath, bbox)
        return bbox

        # get bounding boxes for list of frames

    def getBboxes_framelist(self, frames):
        bbox_list = list()
        for i in range(len(frames)):
            bbox_list.append(self.detect_boxes(frames[i]))
        return bbox_list

        # detection bounding box to dict

    def box_to_dict(self, box, class_id):
        b = {"id": class_id, "x1": box[1], "x2": box[3], "y1": box[0], "y2": box[2]}
        return b

        # upscale one bbox

    def upscale_bbox(self, bbox, scale):
        x1 = bbox["x1"] * scale
        x2 = bbox["x2"] * scale
        y1 = bbox["y1"] * scale
        y2 = bbox["y2"] * scale
        class_id = bbox["id"]
        b = {"id": class_id, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
        return b

        # upscale list of lists of bboxes

    def upscale_all_bboxes(self, bbox_list, scale):
        upscaled_bboxes = list()
        for i in range(len(bbox_list)):
            boxes = list()
            for j in bbox_list[i]:
                boxes.append(self.upscale_bbox(j, scale))
            upscaled_bboxes.append(boxes)
            del boxes
        return upscaled_bboxes

        # upscale list of bboxes

    def upscale_bboxes_list(self, bbox_list, scale):
        upscaled_bboxes = list()
        for i in bbox_list:
            upscaled_bboxes.append(self.upscale_bbox(i, scale))
        return upscaled_bboxes

        # only for debugging

    def drawBox(self, image, box):
        # cv2 colors are in BGR instead of RGB
        colors = {0: (0, 255, 2550), 1: (0, 0, 255), 2: (255, 255, 0), 3: (255, 0, 0)}
        y1 = (int)(box["y1"])
        x1 = (int)(box["x1"])
        y2 = (int)(box["y2"])
        x2 = (int)(box["x2"])
        class_id = (int)(box["id"])

        image = cv2.rectangle(image, (x1, y1), (x2, y2), colors[class_id], 2)

        return image

        # calculate linear boxes between two bounding boxes

    def bbox_mean(self, first_box, second_box, lenght):
        # Points from boxes
        b1p1 = [first_box["x1"], first_box["y1"]]
        b1p2 = [first_box["x2"], first_box["y2"]]

        b2p1 = [second_box["x1"], second_box["y1"]]
        b2p2 = [second_box["x2"], second_box["y2"]]

        # calculate vectors between matching points
        vec_p1 = np.subtract(b2p1, b1p1)
        vec_p2 = np.subtract(b2p2, b1p2)

        # calculate sections with mean
        factor = (lenght + 1) ** (-1)
        new_p1 = np.add(b1p1, np.dot(vec_p1, factor))
        new_p2 = np.add(b1p2, np.dot(vec_p2, factor))
        new_p1 = (np.rint(new_p1)).astype(int)
        new_p2 = (np.rint(new_p2)).astype(int)

        class_id = (first_box["id"])
        boxes = list()
        for i in range(1, lenght + 1):
            y1 = new_p1[1]
            x1 = new_p1[0]
            y2 = new_p2[1]
            x2 = new_p2[0]
            boxes.append(self.make_bbox(x1, x2, y1, y2, class_id))
            new_p1 = np.add(new_p1, np.dot(vec_p1, factor))
            new_p2 = np.add(new_p2, np.dot(vec_p2, factor))
            new_p1 = (np.rint(new_p1)).astype(int)
            new_p2 = (np.rint(new_p2)).astype(int)
        return boxes

        # bbox by polynominal interpolation for list of frames

    def calculate_bbox_interpolation_center(self, last_bboxes, current_box, frames):
        x = list()
        y = list()
        # get center point of box for interpolation
        for box in last_bboxes:
            y1 = (int)(box["y1"])
            x1 = (int)(box["x1"])
            y2 = (int)(box["y2"])
            x2 = (int)(box["x2"])

            x_center = (int)((x1 + x2) / 2)
            y_center = (int)((y1 + y2) / 2)
            x.append(x_center)
            y.append(y_center)

        # current_box values
        y1 = (int)(current_box["y1"])
        x1 = (int)(current_box["x1"])
        y2 = (int)(current_box["y2"])
        x2 = (int)(current_box["x2"])

        x_center = (int)((x1 + x2) / 2)
        y_center = (int)((y1 + y2) / 2)
        x.append(x_center)
        y.append(y_center)

        # interpolation with numpy
        param = np.polyfit(x, y, 2)

        # choose new x for frame by distance beween last 2 bboxes
        x_new = self.get_interpolation_x_values(x[-1], x[-2], len(frames))
        y_new = list()
        for value in x_new:
            y_pred = self.pred_y_degree_2(value, param[0], param[1], param[2])
            y_new.append(y_pred)

        bboxes = list()
        # get corners of bbox for calculated center
        # use with and height of last bbox
        last_box = last_bboxes[-1]
        width = box["x2"] - box["x1"]
        height = box["y2"] - box["y1"]
        for i in len(x_new):
            x1 = (int)(x_new[i] - (width / 2))
            x2 = (int)(x_new[i] + (width / 2))
            y1 = (int)(y_new[i] - (height / 2))
            y2 = (int)(y_new[i] + (height / 2))
            bboxes.append(self.make_bbox(x1, x2, y1, y2, 0))

        return bboxes

        # bbox by polynominal interpolation for list of frames

    def calculate_bbox_interpolation_corners(self, last_bboxes, current_box, frames):
        x1 = list()
        x2 = list()
        y1 = list()
        y2 = list()
        # get center point of box for interpolation
        for box in last_bboxes:
            y1_b = (int)(box["y1"])
            x1_b = (int)(box["x1"])
            y2_b = (int)(box["y2"])
            x2_b = (int)(box["x2"])

            x1.append(x1_b)
            x2.append(x2_b)
            y1.append(y1_b)
            y2.append(y2_b)

        # current_box values
        y1_b = (int)(current_box["y1"])
        x1_b = (int)(current_box["x1"])
        y2_b = (int)(current_box["y2"])
        x2_b = (int)(current_box["x2"])

        x1.append(x1_b)
        x2.append(x2_b)
        y1.append(y1_b)
        y2.append(y2_b)

        # interpolation with numpy
        param_p1 = np.polyfit(x1, y1, 2)
        param_p2 = np.polyfit(x2, y2, 2)

        # choose new x for frame by distance beween last 2 bboxes
        x1_new = self.get_interpolation_x_values(x1[-1], x1[-2], len(frames))
        x2_new = self.get_interpolation_x_values(x2[-1], x2[-2], len(frames))
        y1_new = list()
        y2_new = list()
        for value in x_new:
            y1_pred = self.pred_y_degree_2(value, param_p1[0], param_p1[1], param_p1[2])
            y1_new.append(y1_pred)
            y2_pred = self.pred_y_degree_2(value, param_p2[0], param_p2[1], param_p2[2])
            y2_new.append(y2_pred)

        bboxes = list()
        # get corners of bbox for calculated center
        # use with and height of last bbox
        for i in len(x_new):
            b_x1 = (int)(x1_new[i])
            b_x2 = (int)(x2_new[i])
            b_y1 = (int)(y1_new[i])
            b_y2 = (int)(y2_new[i])
            bboxes.append(self.make_bbox(b_x1, b_x2, b_y1, b_y2, 0))

        return bboxes

    def pred_y_degree_2(self, x_value, a, b, c):

        y = a * x_value ** 2 + b * x_value + c
        return y

    def get_interpolation_x_values(self, last_x, second_to_last_x, number_of_values):
        distance = last_x - second_to_last_x

        # sections
        factor = (number_of_values + 1) ** (-1)
        x_values = list()
        for i in range(1, number_of_values + 1):
            boxes.append(new_x)
            new_x = new_x + distance * factor
            new_x = (int)(round(new_x))
        return x_values

        # create bbox as dict from values

    def make_bbox(self, x1, x2, y1, y2, class_id):
        b = {"id": class_id, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
        return b




