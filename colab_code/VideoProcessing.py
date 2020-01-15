import os
import queue
import cv2

from colab_code.Cropping import Cropping
from colab_code.RiderDetector import RiderDetector
from colab_code.VideoQuality import VideoQuality


class VideoProcessing:

    def __init__(self, path_weights):
        self.detector = RiderDetector(path_weights)
        self.cropper = Cropping()
        self.vidQuality = VideoQuality()

    def process_frames(self, video_path):
        video = cv2.VideoCapture(video_path)
        filename = os.path.basename(video_path)
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

        print(total_frames)

        fps = video.get(cv2.CAP_PROP_FPS)

        # Check for first picture
        success, img = video.read()

        sizeX = 800  # HD
        sizeY = 450
        size = (sizeX, sizeY)
        ratio = sizeX / sizeY

        downscale_factor = 0.5

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter('/content/drive/My Drive/CV Praktikum/Cropping.mp4', fourcc, fps, size)

        for i in range(int(total_frames), desc='extract frames'):

            if success:

                # downsize frame and detect
                downsize_img = self.downscale_frame(img, downscale_factor)
                bboxes = self.detector.detect_boxes(downsize_img)

                # calculate missing bboxes and scale them up
                bboxes = self.detector.upscale_bboxes_list(bboxes, (downscale_factor ** (-1)))

                # crop frame
                box = self.cropper.complete_bbox(img, bboxes)

                for b in bboxes:
                    img = self.detector.drawBox(img, b)

                cropped_frame = self.cropper.crop_image(box, img)
                if i < 50:
                    cv2.imwrite("/content/drive/My Drive/CV Praktikum/video11_analyse/frames2/frame%d.jpg" % i, img)

                # resize picture to output size
                img = cv2.resize(cropped_frame, size)

                out.write(img)
            del img
            success, img = video.read()
        video.release();
        out.release()

        # dectect not every frame

    def process_frames_faster(self, video_path):
        video = cv2.VideoCapture(video_path)
        filename = os.path.basename(video_path)
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

        print(total_frames)

        fps = video.get(cv2.CAP_PROP_FPS)
        print(fps)

        # Check for first picture
        success, img = video.read()

        sizeX = 800  # HD
        sizeY = 450
        size = (sizeX, sizeY)
        ratio = sizeX / sizeY

        downscale_factor = 0.5

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter('/content/drive/My Drive/CV Praktikum/Cropping.mp4', fourcc, fps, size)

        skip_frames_number = 5

        last_frames = list()
        last_bboxes = list()

        for i in range(int(total_frames), desc='extract frames'):

            if success:

                if len(last_frames) == skip_frames_number or i < skip_frames_number or skip_frames_number == 0:

                    # downsize frame and detect
                    downsize_img = self.downscale_frame(img, downscale_factor)
                    bboxes = self.detector.detect_boxes(downsize_img)

                    # calculate missing bboxes and scale them up
                    bboxes = self.detector.upscale_bboxes_list(bboxes, (downscale_factor ** (-1)))

                    # crop frame
                    box = self.cropper.complete_bbox(img, bboxes)

                    # if(len(bboxes)==0):
                    # box=self.vidQuality.calculate_missing_bbox_last_frames(last_bboxes)

                    cropped_frame = self.cropper.crop_image(box, img)

                    # calculate cropping of left out frames
                    if len(last_frames) == skip_frames_number and skip_frames_number > 0:
                        # last_frames.reverse()
                        last_frames = self.calculate_missing_frames(last_bboxes[0], box, last_frames)
                        last_frames = self.resize_frames(last_frames, size)
                        for frame in last_frames:
                            out.write(frame)
                        last_frames.clear()

                    # save calculated box for frame
                    if len(last_bboxes) >= 1:
                        last_bboxes.pop(0)
                    last_bboxes.append(box)

                    # resize picture to output size
                    img = cv2.resize(cropped_frame, size)
                    out.write(img)

                # skip and save frames
                else:
                    if len(last_frames) >= skip_frames_number:
                        last_frames.pop(0)
                    last_frames.append(img)

            del img
            success, img = video.read()
        video.release();
        out.release()

        # dectect not every frame

    def process_frames_faster2(self, video_path):
        video = cv2.VideoCapture(video_path)
        filename = os.path.basename(video_path)
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

        print(total_frames)

        fps = video.get(cv2.CAP_PROP_FPS)
        print(fps)

        # Check for first picture
        success, img = video.read()

        sizeX = 800  # HD
        sizeY = 450
        size = (sizeX, sizeY)
        ratio = sizeX / sizeY

        downscale_factor = 0.5

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter('/content/drive/My Drive/CV Praktikum/Cropping.mp4', fourcc, fps, size)

        last_bboxes = list()
        last_frames = list()

        bbox_lenght = 5
        skip_frames_number = 5

        for i in range(int(total_frames), desc='extract frames'):

            if success:
                # detection of each nth frame
                if len(last_bboxes) < bbox_lenght or skip_frames_number == 5 or len(
                        last_frames) == skip_frames_number or skip_frames_number == 0:

                    # downsize frame and detect
                    downsize_img = self.downscale_frame(img, downscale_factor)
                    bboxes = self.detector.detect_boxes(downsize_img)

                    # calculate missing bboxes and scale them up
                    bboxes = self.detector.upscale_bboxes_list(bboxes, (downscale_factor ** (-1)))

                    # crop frame
                    box = self.cropper.complete_bbox(img, bboxes)
                    cropped_frame = self.cropper.crop_image(box, img)

                    if len(last_frames) == skip_frames_number and skip_frames_number > 0:
                        calculate_last_bboxes = self.detector.calculate_bbox_interpolation_corners(last_bboxes, box,
                                                                                                   last_frames)
                        for i in len(last_frames):
                            box = self.cropper.complete_bbox(last_frames[i], [calculate_last_bboxes[i]])
                            cropped_frame = self.cropper.crop_image(box, last_frames[i])
                            last_frames = self.resize_frames(last_frames, size)
                            out.write(last_frames[i])
                        last_frames.clear()

                    # resize picture to output size
                    img = cv2.resize(cropped_frame, size)
                    out.write(img)

                    # save calculated box for frame
                    if len(last_bboxes) >= bbox_lenght:
                        last_bboxes.pop(0)
                    last_bboxes.append(box)
                    counter = 0

                # safe frames for interpolation of bboxes
                else:
                    if len(last_frames) >= skip_frames_number:
                        last_frames.pop(0)
                    last_frames.append(img)

            del img
            success, img = video.read()
        video.release();
        out.release()

        # crop left out frames

    def calculate_missing_frames(self, box, old_bbox, frames):
        calculated_boxes = self.detector.bbox_mean(box, old_bbox, len(frames))
        cropped_frames = self.cropper.crop_image_list(calculated_boxes, frames)
        return cropped_frames

        # downscale list of frames by factor

    def downscale_frames(self, frames, scale_factor):
        small_frames = list()
        for i in range(len(frames), desc='downsize frames'):
            small_frames.append(self.downscale_frame(frames[i], scale_factor))
        return small_frames

        # downscale one frame

    def downscale_frame(self, frame, scale):
        return cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    def make_bbox(self, x1, x2, y1, y2, class_id):
        b = {"id": class_id, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
        return b

        # resize list of frame with opencv

    def resize_frames(self, frames, size):
        resized_frames = list()
        for f in frames:
            resized_frames.append(cv2.resize(f, size))
        return resized_frames

        # videoclip = mpe.VideoFileClip(filename.strip('.MP4') + 'Crop.mp4')
        # Audiostuff, takes alot longer tho
        # audioclip = mpe.CompositeAudioClip([mpe.AudioFileClip(video_path)])
        # videoclip.audio = audioclip
        # videoclip.write_videofile(filename.strip('.mp4')+'Crop.mp4')