import sys
from Mainwindow import Mainwindow
from PyQt5.QtWidgets import QApplication

from colab_code.VideoProcessing import VideoProcessing


def main():
    a = QApplication(sys.argv)
    w = Mainwindow()
    w.show()
    return a.exec_()

def mainNoGui():
    model_path='D:\Programming\mask_rcnn_rider_cfg_0125.h5'
    video_path='C:/Users/Tabea/Videos/1sec.mp4'
    v=VideoProcessing(model_path)
    v.process_frames(video_path)


if __name__ == '__main__':
    mainNoGui()
