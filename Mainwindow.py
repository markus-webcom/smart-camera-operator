from Ui import Ui
import numpy as np
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QErrorMessage
from videoToFrames import VideoToFrames
import cv2 as opencv


class Mainwindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_video = None
        self.setup_ui()
        self.connect_buttons()
        self.center_and_rescale()
        self.ui.progress_bar.hide()

    def setup_ui(self):
        self.ui = Ui(self)
        self.ui.setup()

    def center_and_rescale(self):
        desktop = QDesktopWidget()
        self.move(desktop.availableGeometry(desktop.primaryScreen()).center())
        self.resize(150, 150)

    def connect_buttons(self):
        self.ui.open_video_button.clicked.connect(self.open_video_button_clicked)
        self.ui.start_button.clicked.connect(self.start_clicked)

    def start_clicked(self):
        if self.selected_video is not None:
            self.ui.progress_bar.show()
            VideoToFrames().crop(self.selected_video, self.ui.progress_bar)
            self.ui.progress_bar.hide()
        else:
            self.show_no_video_error()

    def open_video_button_clicked(self):
        self.selected_video = self.request_video_path()

    def request_video_path(self):
        return QFileDialog.getOpenFileName(self, 'Open video(mp4)...', '', 'Video Files (*.mp4)')[0]

    def show_no_video_error(self):
        error = QErrorMessage(self)
        error.setWindowTitle('No video selected')
        error.showMessage('You have not selected a video yet. Please load a video first.')

    # Override, damit Fenster schließbar ist
    def closeEvent(self, event):
        event.accept()
