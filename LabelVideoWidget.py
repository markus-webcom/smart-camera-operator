import sys
import cv2
from os.path import join
import os
from Operator import Operator
import fnmatch

#from PyQt5.QtGui import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.QtCore import Qt

class LabelVideoWidget(QWidget):
    def __init__(self, parent=None):
        super(LabelVideoWidget, self).__init__(parent)
        self.operator = None
        self.counter = 0
        self.num_files=0

        self.inputFile = None
        self.inputFolder=None
        self.image_name=None
        self.frame_number=0
        self.n=20
        self.label_counter=0

        # Buttons
        self.AcceptBTN = QPushButton('Accept', self)
        self.DiscardBTN = QPushButton('Discard', self)
        self.chooseFolderBTN = QPushButton('Choose Video', self)
        self.goTrainBTN = QPushButton('Train with labeled data', self)
        self.goTrainBTN.setEnabled(False)
        self.returnStartBTN = QPushButton('Startpage', self)
        self.acceptAllBTN=QPushButton('Accept all', self)

        self.DiscardBTN.clicked.connect(self.discard_clicked)
        self.AcceptBTN.clicked.connect(self.accept_clicked)
        self.chooseFolderBTN.clicked.connect(self.clicked_chooseFolderBTN)
        self.acceptAllBTN.clicked.connect(self.acceptAll_clicked)

        # Display for pictures as pixmap
        self.picDisplay = QLabel('proxy for pictures')

        # progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setMaximum(0)
        self.progressBar.setVisible(False)

        # Format Layout



        layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()

        hbox.addWidget(self.AcceptBTN)
        hbox.addWidget( self.acceptAllBTN)
        hbox.addWidget(self.DiscardBTN)

        hbox2.addWidget(QLabel(''))
        hbox2.addWidget(self.returnStartBTN)
        hbox2.setAlignment(Qt.AlignRight)

        layout.addWidget(self.chooseFolderBTN)
        layout.addLayout(hbox)
        layout.addWidget(self.goTrainBTN)

        layout.addWidget(self.picDisplay)
        layout.addWidget(self.progressBar)
        layout.addLayout(hbox2)
        layout.setSpacing(25)



        # setLayout in Window
        self.setLayout(layout)

    def getTrainDir(self):
        return self.img_save_path

    def setOperator(self, new_operator):
        self.operator = new_operator

    def discard_clicked(self):
        if (self.counter > 0):
            self.progressBar.setValue(self.counter)
            QApplication.processEvents()

        if (self.inputFile is not None):
            self.counter += 1
            print(self.n * self.counter, self.frame_number)

            if( self.n*self.counter<self.frame_number):
                self.image_name=('_frame(%d).png' % self.counter)
                self.image_name=self.vid_name+self.image_name

                frame=self.operator.getNthFrameFromVideo(self.inputFile,self.n*self.counter)
                self.cvImg = frame.copy()
                print(self.cvImg.shape)
                img=self.cvImg.copy()
                cvImg_with_boxes, self.boxes = self.operator.drawBoxes(img)

                image = QImage(cvImg_with_boxes, cvImg_with_boxes.shape[1], \
                           cvImg_with_boxes.shape[0], cvImg_with_boxes.shape[1] * 3,
                           QImage.Format_RGB888).rgbSwapped()

                pixmap = QPixmap(image)

                bigger_pixmap = pixmap.scaled(2000, 1500, Qt.KeepAspectRatio)

                self.picDisplay.setPixmap(bigger_pixmap)

        print('discard')

    def clicked_chooseFolderBTN(self):
        # FileDialog to choose folder
        self.counter = 0
        self.label_counter = 0
        self.picDisplay.setText('Waiting')
        self.inputFile = QFileDialog.getOpenFileName(self, 'Open video(mp4)...', '', 'Video Files (*.mp4)')[0]
        self.vid_name=os.path.basename(self.inputFile)
        self.vid_name=os.path.splitext(self.vid_name)[0]
        if (self.inputFile != ''):
                self.loadFile()

    def loadFile(self):
        self.frame_number = self.operator.getNumberVideoFrames(self.inputFile)
        self.discard_clicked()

        self.inputFolder = os.path.dirname(self.inputFile)
        self.img_save_path = os.path.normpath(join(self.inputFolder, 'accepted_images'))
        if not os.path.exists(self.img_save_path):
            os.makedirs(self.img_save_path)

        self.db_path = join(self.img_save_path, 'annotations')
        self.db_path = os.path.normpath(self.db_path)
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

        self.progressBar.setMaximum(int(self.frame_number / self.n))
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)

        self.num_files = len(fnmatch.filter(os.listdir(self.db_path), '*.csv'))
        if (self.num_files > 1):
            self.goTrainBTN.setEnabled(True)



    def accept_clicked(self):
        if (self.inputFolder is not None):
            self.label_counter+=1
            if not self.progressBar.isVisible() and self.label_counter > 1:
                self.goTrainBTN.setEnabled(True)
            fileName, fileExtension = os.path.splitext(self.image_name)
            image_save_path = join(self.img_save_path, self.image_name)
            database_path = join(self.db_path, fileName + '.csv')

            cv2.imwrite(image_save_path,self.cvImg)
            height = self.cvImg.shape[0]
            width = self.cvImg.shape[1]
            self.operator.writeBboxesToCsv(database_path, self.image_name, self.boxes, height,width)

            self.discard_clicked()
        print('accept')

    def acceptAll_clicked(self):
        if (self.inputFolder is not None):
            while(self.n*self.counter<self.frame_number):
                self.accept_clicked()
