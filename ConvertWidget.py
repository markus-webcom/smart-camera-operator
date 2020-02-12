import sys

#from PyQt5.QtGui import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class ConvertWidget(QWidget):
    def __init__(self, parent=None):
        super(ConvertWidget, self).__init__(parent)

        self.ConvertBTN = QPushButton('Convert', self)
        self.ChooseFileBTN=QPushButton('Choose Video File',self)
        self.returnStartBTN=QPushButton('Start',self)

        self.ConvertBTN.clicked.connect(self.convertClicked)
        self.ChooseFileBTN.clicked.connect(self.chooseFileClicked)

        # progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setMaximum(0)
        self.progressBar.setVisible(False)


        layout = QVBoxLayout()
        hbox=QHBoxLayout()
        hbox.addWidget(QLabel(''))
        hbox.addWidget(self.returnStartBTN)
        hbox.setAlignment(Qt.AlignRight)
        layout.addWidget(self.ChooseFileBTN)
        layout.addWidget(self.ConvertBTN)
        layout.addWidget(self.progressBar)
        layout.addLayout(hbox)

        self.setLayout(layout)

        self.operator=None
        self.inputFile=None

    def setOperator(self,new_operator):
        self.operator=new_operator

    def convertClicked(self):
        if self.inputFile is not None:
            self.operator.convertVideo(self.inputFile,self.progressBar)
            #self.progressBar.hide()


    def chooseFileClicked(self):
        self.inputFile = QFileDialog.getOpenFileName(self, 'Open video(mp4)...', '', 'Video Files (*.mp4)')[0]
