import sys

#from PyQt5.QtGui import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class StartWidget(QWidget):
    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)

        # Buttons
        self.LabelBTN=QPushButton('Label more pictures', self)
        self.ConvertBTN = QPushButton('Convert Video', self)

        # Format Layout
        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.LabelBTN)
        layout.addWidget(self.ConvertBTN)


        # setLayout in Window
        self.setLayout(layout)

