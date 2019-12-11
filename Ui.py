from PyQt5.QtWidgets import *


class Ui:
    def __init__(self, parent):
        self.parent = parent

    def setup(self):
        self.main_widget = QWidget(self.parent)
        self.main_widget.setLayout(QVBoxLayout())
        self.parent.setCentralWidget(self.main_widget)

        self.open_video_button = QPushButton(self.parent)
        self.open_video_button.setText("Load Video")
        self.main_widget.layout().addWidget(self.open_video_button)

        self.start_button = QPushButton(self.parent)
        self.start_button.setText("Start")
        self.main_widget.layout().addWidget(self.start_button)

        self.progress_bar = QProgressBar(self.parent)
        self.main_widget.layout().addWidget(self.progress_bar)
