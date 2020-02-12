import sys

#from PyQt5.QtGui import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class ConvertWidget(QWidget):
    def __init__(self, parent=None):
        super(ConvertWidget, self).__init__(parent)

        self.ConvertPreciseBTN = QPushButton('Convert precise for each frame', self)
        self.ConvertQuickBTN = QPushButton('Convert with interpolation', self)
        self.ChooseFileBTN=QPushButton('Choose Video File',self)
        self.returnStartBTN=QPushButton('Startpage',self)

        self.ConvertPreciseBTN.clicked.connect(self.convertPreciseClicked)
        self.ChooseFileBTN.clicked.connect(self.chooseFileClicked)
        self.ConvertQuickBTN.clicked.connect(self.convertQuickClicked)




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
        layout.addWidget(self.ConvertPreciseBTN)
        layout.addWidget(self.ConvertQuickBTN)
        layout.addWidget(self.progressBar)
        layout.addLayout(hbox)

        layout.setSpacing(50)


        self.setLayout(layout)

        self.operator=None
        self.inputFile=None

    def setOperator(self,new_operator):
        self.operator=new_operator

    def convertQuickClicked(self):
        if self.inputFile is not None:
            self.operator.convertQuickVideo(self.inputFile,self.progressBar)
            self.progressBar.hide()

    def convertPreciseClicked(self):
        if self.inputFile is not None:
            self.operator.convertPreciseVideo(self.inputFile,self.progressBar)
            self.progressBar.hide()


    def chooseFileClicked(self):
        self.inputFile = QFileDialog.getOpenFileName(self, 'Open video(mp4)...', '', 'Video Files (*.mp4)')[0]
