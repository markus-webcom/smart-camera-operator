import sys

#from PyQt5.QtGui import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class StartWidget(QWidget):
    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)

        # Buttons
        self.LabelBTN=QPushButton('Label more data', self)
        self.ConvertBTN = QPushButton('Convert video', self)


        # Format Layout
        layout = QVBoxLayout()

        #layout.setAlignment(Qt.AlignCenter)
        #layout.setSpacing(50)
        #self.LabelBTN.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        #self.ConvertBTN.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))



        layout.addWidget(self.LabelBTN)
        layout.addWidget(self.ConvertBTN)
        layout.setSpacing(50)


        # setLayout in Window
        self.setLayout(layout)

