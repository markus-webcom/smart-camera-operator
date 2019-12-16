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
        pass

    def crop(self, frames_with_boxes: list) -> list:
        pass

    def make_video(self, cropped_frames: list):
        pass

    def get_frames(self, video_path: str) -> list:
        pass
