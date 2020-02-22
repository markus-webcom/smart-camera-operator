from scipy.ndimage import gaussian_filter1d
from colab_code.BoundingBox import BoundingBox


class VideoQuality:
    # get last bbox if none found in current frame
    def fill_missing_bboxes(self, bboxes):
        for i in range(len(bboxes)):
            if len(bboxes[i]) == 0 and i > 0:
                bboxes[i] = bboxes[i - 1]
        return bboxes

    # calculate bbox by last 2 frames
    def calculate_missing_bbox_last_frames(self, bboxes):
        if bboxes.empty():
            return BoundingBox(-1, -1, -1, -1, 0)
        if bboxes.qsize() == 1:
            return bboxes.get()
        while bboxes.qsize() > 2:
            bboxes.get()
        # bboxes from last 2 frames
        second = bboxes.get()
        first = bboxes.get()

        box = self.mean_boxes(first, second)
        return box

    def mean_boxes(self, first, second):
        x1 = int((first.getX1() + second.getX1()) / 2)
        x2 = int((first.getX2() + second.getX2()) / 2)
        y1 = int((first.getY1() + second.getY1()) / 2)
        y2 = int((first.getY2() + second.getY2()) / 2)
        return BoundingBox(x1, x2, y1, y2, 0)

    def smooth_boxes(self, boxes: list):
        sigma = 5
        gaussX1 = gaussian_filter1d([int(box.getX1()) for box in boxes], sigma)
        gaussX2 = gaussian_filter1d([int(box.getX2()) for box in boxes], sigma)
        gaussY1 = gaussian_filter1d([int(box.getY1()) for box in boxes], sigma)
        gaussY2 = gaussian_filter1d([int(box.getY2()) for box in boxes], sigma)

        for i in range(0, len(boxes)):
            class_id = boxes[i].getClassId()
            boxes[i] = BoundingBox(gaussX1[i], gaussX2[i], gaussY1[i], gaussY2[i], class_id)
        return boxes
