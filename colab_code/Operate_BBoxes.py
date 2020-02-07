from colab_code.BoundingBox import BoundingBox
import numpy as np
class Operate_BBoxes:
    # upscale list of bboxes
    def scale_bboxes_list(self, bbox_list, scale):
        for i in bbox_list:
            i.scale_bbox(scale)


    # calculate linear boxes between two bounding boxes
    def bbox_mean(self, first_box, second_box, number_boxes_between):
        # Points from boxes
        b1p1 = [first_box.getX1(), first_box.getY1()]
        b1p2 = [first_box.getX2(), first_box.getY2()]

        b2p1 = [second_box.getX1(), second_box.getY1()]
        b2p2 = [second_box.getX2(), second_box.getY2()]

        # calculate vectors between matching points
        vec_p1 = np.subtract(b2p1, b1p1)
        vec_p2 = np.subtract(b2p2, b1p2)

        # calculate sections with mean
        factor = (number_boxes_between + 1) ** (-1)
        new_p1 = np.add(b1p1, np.dot(vec_p1, factor))
        new_p2 = np.add(b1p2, np.dot(vec_p2, factor))
        new_p1 = (np.rint(new_p1)).astype(int)
        new_p2 = (np.rint(new_p2)).astype(int)

        class_id = first_box.getClassId()
        boxes = list()
        for i in range(1, number_boxes_between + 1):
            y1 = new_p1[1]
            x1 = new_p1[0]
            y2 = new_p2[1]
            x2 = new_p2[0]
            boxes.append(BoundingBox(x1, x2, y1, y2, class_id))
            new_p1 = np.add(new_p1, np.dot(vec_p1, factor))
            new_p2 = np.add(new_p2, np.dot(vec_p2, factor))
            new_p1 = (np.rint(new_p1)).astype(int)
            new_p2 = (np.rint(new_p2)).astype(int)
        return boxes

    # bbox by polynominal interpolation for list of frames
    def calculate_bbox_interpolation_center(self, last_bboxes, current_box, number_boxes_between):
        x = list()
        y = list()
        # get center point of box for interpolation
        for box in last_bboxes:
            x_center = int((box.getX1() + box.getX2()) / 2)
            y_center = int((box.getY1() + box.getY2()) / 2)
            x.append(x_center)
            y.append(y_center)

        # current_box values
        x_center = int((current_box.getX1() + current_box.getX2()) / 2)
        y_center = int((current_box.getY1() + current_box.getY2()) / 2)
        x.append(x_center)
        y.append(y_center)


        # interpolation with numpy
        param = np.polyfit(x, y, 2)

        # choose new x for frame by distance beween last 2 bboxes
        x_new = self.get_interpolation_x_values(x[-1], x[-2], number_boxes_between)
        y_new = list()
        for value in x_new:
            y_pred = self.pred_y_degree_2(value, param[0], param[1], param[2])
            y_new.append(y_pred)

        bboxes = list()
        # get corners of bbox for calculated center
        # use with and height of last bbox
        last_box = last_bboxes[-1]
        width = last_box.getX2() - last_box.getX1()
        height = last_box.getY2() - last_box.getY1()
        for i in range(len(x_new)):
            x1 = int(x_new[i] - (width / 2))
            x2 = int(x_new[i] + (width / 2))
            y1 = int(y_new[i] - (height / 2))
            y2 = int(y_new[i] + (height / 2))
            bboxes.append(BoundingBox(x1, x2, y1, y2, 0))
        return bboxes

        # bbox by polynominal interpolation for list of frames

    def calculate_bbox_interpolation_corners(self, last_bboxes, current_box, number_boxes_between):
        x1 = list()
        x2 = list()
        y1 = list()
        y2 = list()
        # get center point of box for interpolation
        for box in last_bboxes:
            x1.append(box.getX1())
            x2.append(box.getX2())
            y1.append(box.getY1())
            y2.append(box.getY2())

        # current_box values
        x1.append(current_box.getX1())
        x2.append(current_box.getX2())
        y1.append(current_box.getY1())
        y2.append(current_box.getY2())

        # interpolation with numpy
        param_p1 = np.polyfit(x1, y1, 2)
        param_p2 = np.polyfit(x2, y2, 2)

        # choose new x for frame by distance beween last 2 bboxes
        x1_new = self.get_interpolation_x_values(x1[-1], x1[-2], number_boxes_between)
        x2_new = self.get_interpolation_x_values(x2[-1], x2[-2], number_boxes_between)

        y1_new = list()
        y2_new = list()
        for value in x1_new:
            y1_pred = self.pred_y_degree_2(value, param_p1[0], param_p1[1], param_p1[2])
            y1_new.append(y1_pred)
            y2_pred = self.pred_y_degree_2(value, param_p2[0], param_p2[1], param_p2[2])
            y2_new.append(y2_pred)

        bboxes = list()
        # get corners of bbox for calculated center
        # use with and height of last bbox
        for i in range(len(x1_new)):
            b_x1 = int(x1_new[i])
            b_x2 = int(x2_new[i])
            b_y1 = int(y1_new[i])
            b_y2 = int(y2_new[i])
            bboxes.append(BoundingBox(b_x1, b_x2, b_y1, b_y2, 0))

        return bboxes

    # calculate values for polynominal function of degree 2 ax^2+bx+c
    def pred_y_degree_2(self, x_value, a, b, c):
        y = a * x_value ** 2 + b * x_value + c
        return y

    def get_interpolation_x_values(self, last_x, second_to_last_x, number_of_values):
        distance = last_x - second_to_last_x

        # sections
        factor = (number_of_values + 1) ** (-1)
        x_values = list()
        new_x = second_to_last_x + distance * factor
        new_x = int(round(new_x))
        for i in range(1, number_of_values + 1):
            x_values.append(new_x)
            new_x = new_x + distance * factor
            new_x = int(round(new_x))
        return x_values


