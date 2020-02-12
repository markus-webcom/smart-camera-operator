import cv2
from tqdm import tnrange
from colab_code.Cropping import Cropping
from colab_code.RiderDetector import RiderDetector
from colab_code.VideoQuality import VideoQuality


class VideoProcessing:

    def __init__(self, path_weights, progress_bar):
        self.detector = RiderDetector(path_weights)
        self.cropper = Cropping()
        self.vidQuality = VideoQuality()
        self.progress_bar = progress_bar
        self.size = (800, 450)
        self.fps = 0

    def test_video(self, path):

        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = (640, 480)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter('/content/drive/My Drive/CV Praktikum/Test.mp4', fourcc, fps, size)

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, size)
                # write the flipped frame
                out.write(frame)
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()

    def paint_boxes_into_video(self, video_path: str):
        self.process_frames(video_path, crop=False, draw_boxes=True)

    def process_frames(self, video_path: str, crop: bool = True, draw_boxes: bool = False):
        frames = self.get_frames(video_path)
        boxes = self.extract_boxes(frames)
        print('frames : {}'.format(len(frames)))
        print('boxes: {}'.format(len(boxes)))

        if crop:
            frames = self.crop_frames(frames, boxes)

        if draw_boxes:
            frames = self.draw_boxes(frames, boxes)

        self.create_output(frames)

    def process_frames_old(self, video_path: str, crop: bool = True, draw_boxes: bool = False):
        video = cv2.VideoCapture(video_path)
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

        print(total_frames)

        fps = video.get(cv2.CAP_PROP_FPS)

        # Check for first picture
        success, img = video.read()
        size = (800, 450)

        downscale_factor = 1
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter('result.mp4', fourcc, fps, size)

        for i in tnrange(int(total_frames), desc='extract frames'):
            if self.progress_bar is not None:
                self.progress_bar.setValue((i / total_frames) * 100)
            if success:
                # downsize frame and detect
                downsize_img = self.downscale_frame(img, downscale_factor)
                bboxes = self.detector.getBboxes(downsize_img)

                # calculate missing bboxes and scale them up
                bboxes = self.detector.upscale_bboxes_list(bboxes, (downscale_factor ** (-1)))

                if draw_boxes:
                    for b in bboxes:
                        img = self.detector.drawBox(img, b)

                if crop:
                    # crop frame
                    box = self.cropper.complete_bbox(img, bboxes)
                    img = self.cropper.crop_image(box, img)

                # resize picture to output size
                img = cv2.resize(img, size)

                out.write(img)
            del img
            success, img = video.read()
        video.release()
        out.release()

    def downscale_frames(self, frames, scale_factor):
        small_frames = list()
        for i in tnrange(len(frames), desc='downsize frames'):
            small_frames.append(self.downscale_frame(frames[i], scale_factor))
        return small_frames

    def downscale_frame(self, frame, scale):
        return cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    def extract_boxes(self, frames) -> list:
        # Check for first picture
        downscale_factor = 1
        boxes = []

        for img in frames:
            # downsize frame and detect
            downsize_img = self.downscale_frame(img, downscale_factor)
            bboxes = self.detector.getBboxes(downsize_img)
            # calculate missing bboxes and scale them up
            bboxes = self.detector.upscale_bboxes_list(bboxes, (downscale_factor ** (-1)))
            box = self.cropper.complete_bbox(img, bboxes)
            boxes.append(box)

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


    def create_output(self, frames):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter('result.mp4', fourcc, self.fps, self.size)

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

