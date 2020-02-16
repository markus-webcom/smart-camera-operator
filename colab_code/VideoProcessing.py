import cv2
from tqdm import tnrange
from colab_code.Cropping import Cropping
from colab_code.RiderDetector import RiderDetector
from colab_code.VideoQuality import VideoQuality


class VideoProcessing:

    def __init__(self, path_weights, progress_bar=None):
        self.detector = RiderDetector(path_weights)
        self.cropper = Cropping()
        self.videoQuality = VideoQuality()
        self.progress_bar = progress_bar
        self.size = (800, 450)
        self.fps = 0

    def paint_boxes_into_video(self, video_path: str):
        self.process_frames(video_path, crop=False)

    def process_frames(self, video_path: str, crop: bool = True):
        frames = self.get_frames(video_path)

        boxes = self.extract_boxes(frames)
        boxes = self.videoQuality.smooth_boxes(boxes)

        frames = self.crop_frames(frames, boxes) if crop else self.draw_boxes(frames, boxes)

        self.create_output(frames, video_path)

    def downscale_frame(self, frame, scale):
        return cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    def extract_boxes(self, frames) -> list:
        downscale_factor = 1
        boxes = []

        for i in range(0, len(frames)):
            if self.progress_bar is not None:
                self.progress_bar.setValue((i / len(frames)) * 100)

            downsize_img = self.downscale_frame(frames[i], downscale_factor)
            boxes.append(self.detector.getBox(downsize_img))

        return boxes

    def crop_frames(self, frames, boxes):
        cropped_frames = []

        for i in range(0, len(boxes)):
            cropped_frames.append(self.cropper.crop_image(boxes[i], frames[i]))

        return cropped_frames

    def draw_boxes(self, frames, boxes):
        frames_with_boxes = []

        for i in range(0, len(boxes)):
            frames_with_boxes.append(self.detector.drawBox(frames[i], boxes[i]))

        return frames_with_boxes

    def create_output(self, frames: list, video_path: str):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        filename = 'result_{}.mp4'.format(video_path)
        out = cv2.VideoWriter(filename, fourcc, self.fps, self.size)

        for img in frames:
            out.write(cv2.resize(img, self.size))

        out.release()

    def get_frames(self, video_path):
        video = cv2.VideoCapture(video_path)
        self.fps = video.get(cv2.CAP_PROP_FPS)
        success, img = video.read()
        frames = []

        while success:
            frames.append(img)
            success, img = video.read()
        del img
        video.release()

        return frames

