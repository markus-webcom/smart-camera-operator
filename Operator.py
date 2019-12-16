import os

import cv2
from ModelRetriever import ModelRetriever


class Operator:

    def __init__(self):
        pass

    def operate(self, video_path: str):
        """
        :param video_path: path to mp4 video
        :return: mp4 video
        """

        frames = self.get_frames(video_path)
        frames_with_boxes = self.detect(frames)
        cropped_frames = self.crop(frames_with_boxes)

        return self.make_video(cropped_frames)

    def detect(self, frames: list) -> list:
        """
        Gibt eine Dict list zurück
        {frame, box}
        :param frames:
        :return:
        """
        result = []
        weights = os.path.abspath('mask_rcnn_coco.h5')
        model = ModelRetriever().get_model(weights)
        result_from_model = model.detect(frames, verbose=0)


    def crop(self, frames_with_boxes: list) -> list:
        pass

    def make_video(self, cropped_frames: list):
        pass

    def get_frames(self, video_path: str) -> list:
        frames = []
        video = cv2.VideoCapture(video_path)
        success, img = video.read()
        while success:
            frames.append(img)
            success, img = video.read()
        return frames


