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
        self.out = None
        self.video = None

    def paint_boxes_into_video(self, video_path: str):
        self.process_frames(video_path, crop=False)

    def process_frames(self, video_path: str, crop: bool = True):
        self.init(video_path)

        frames = self.get_frames()
        while len(frames) > 0:
            boxes = self.extract_boxes(frames)
            boxes = self.videoQuality.smooth_boxes(boxes)
            frames = self.crop_frames(frames, boxes) if crop else self.draw_boxes(frames, boxes)
            self.write(frames)
            frames = self.get_frames()

        self.shutdown()

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

    def write(self, frames: list):
        for img in frames:
            self.out.write(cv2.resize(img, self.size))

    def get_frames(self):
        success, img = self.video.read()
        frames = []
        number = 10

        while success and (number > 0):
            frames.append(img)
            success, img = self.video.read()
            number = number - 1
        del img

        return frames

    def init(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        self.out = self.get_out_object()

    def get_out_object(self):
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        filename = 'result.mp4'
        return cv2.VideoWriter(filename, fourcc, self.fps, self.size)

    def shutdown(self):
        self.video.release()
        self.out.release()

