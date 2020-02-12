import sys
import cv2
from os.path import join
import os
from Operator import Operator

#from PyQt5.QtGui import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.QtCore import Qt

class LabelWidget(QWidget):
    def __init__(self, parent=None):
        super(LabelWidget, self).__init__(parent)
        self.operator=None
        self.counter=0

        self.inputFolder=None

        # Buttons
        self.LabelImagesBTN = QPushButton('Label Images', self)
        self.LabelVideoBTN = QPushButton('Label Video', self)
        self.returnStartBTN = QPushButton('Start', self)


        # Format Layout
        layout = QVBoxLayout()
        hbox=QHBoxLayout()

        layout.addWidget(self.LabelImagesBTN)
        layout.addWidget(self.LabelVideoBTN)

        hbox.addWidget(QLabel(''))
        hbox.addWidget(self.returnStartBTN)
        hbox.setAlignment(Qt.AlignRight)



        layout.addLayout(hbox)

        # setLayout in Window
        self.setLayout(layout)


