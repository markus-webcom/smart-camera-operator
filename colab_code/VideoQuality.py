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
            return self.make_bbox(-1, -1, -1, -1, 0)
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
        x1 = int((first["x1"] + second["x1"]) / 2)
        x2 = int((first["x2"] + second["x2"]) / 2)
        y1 = int((first["y1"] + second["y1"]) / 2)
        y2 = int((first["y2"] + second["y2"]) / 2)
        return self.make_bbox(x1, x2, y1, y2, 0)

    def make_bbox(self, x1, x2, y1, y2, class_id):
        b = {"id": class_id, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
        return b
