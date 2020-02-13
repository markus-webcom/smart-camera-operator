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

class LabelImagesWidget(QWidget):
    def __init__(self, parent=None):
        super(LabelImagesWidget, self).__init__(parent)
        self.operator=None
        self.counter=0
        self.label_counter = 0

        self.num_files = 0

        self.inputFolder=None

        # Buttons
        self.AcceptBTN = QPushButton('Accept', self)
        self.DiscardBTN = QPushButton('Discard', self)
        self.chooseFolderBTN=QPushButton('Choose Folder with Pictures', self)
        self.goTrainBTN=QPushButton('Train with labeled data', self)
        self.goTrainBTN.setEnabled(False)
        self.returnStartBTN = QPushButton('Startpage', self)

        self.DiscardBTN.clicked.connect(self.discard_clicked)
        self.AcceptBTN.clicked.connect(self.accept_clicked)
        self.chooseFolderBTN.clicked.connect(self.clicked_chooseFolderBTN)


        # Display for pictures as pixmap
        self.picDisplay=QLabel('proxy for pictures')

        # progress bar
        self.progressBar=QProgressBar()
        self.progressBar.setMaximum(0)
        self.progressBar.setVisible(False)


        # Format Layout





        layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2=QHBoxLayout()

        hbox.addWidget(self.AcceptBTN)
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
        layout.setSpacing(30)



        # setLayout in Window
        self.setLayout(layout)

    def getTrainDir(self):
        return self.img_save_path
    def setOperator(self,new_operator):
        self.operator=new_operator
    def clicked_chooseFolderBTN(self):
        # FileDialog to choose folder
        self.counter=0
        self.label_counter = 0
        self.picDisplay.setText('Waiting')

        self.inputFolder = QFileDialog.getExistingDirectory(self, 'Select image directory')

        if(self.inputFolder != ''):
            self.loadFiles()

    def loadFiles(self):
        self.images = [f for f in os.listdir(self.inputFolder) if f.endswith(".png")]

        self.img_save_path = os.path.normpath(join(self.inputFolder, 'accepted_images'))
        if not os.path.exists(self.img_save_path):
            os.makedirs(self.img_save_path)

        self.db_path = join(self.img_save_path, 'annotations')
        self.db_path = os.path.normpath(self.db_path)
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        self.num_files = len(fnmatch.filter(os.listdir(self.db_path), '*.csv'))
        if (self.num_files > 1):
            self.goTrainBTN.setEnabled(True)

        self.progressBar.setMaximum(len(self.images))
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)

        self.discard_clicked()


    def discard_clicked(self):
        if(self.inputFolder is not None):
            if(self.counter<len(self.images)):
                self.image_name=self.images[self.counter]
                print(self.image_name)
                image_path = join(self.inputFolder, self.image_name)

                self.cvImg = cv2.imread(image_path)
                print(self.cvImg.shape)

                cvImg_with_boxes,self.boxes = self.operator.drawBoxes(self.cvImg.copy())

                image = QImage(cvImg_with_boxes, cvImg_with_boxes.shape[1], \
                             cvImg_with_boxes.shape[0], cvImg_with_boxes.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()

                pixmap = QPixmap(image)

                bigger_pixmap = pixmap.scaled(1000, 1000, Qt.KeepAspectRatio)

                self.picDisplay.setPixmap(bigger_pixmap)

                self.counter += 1
            if(self.counter>1):
                self.progressBar.setValue(self.counter-1)

        print('discard')

    def accept_clicked(self):
        if(self.inputFolder is not None):
            self.label_counter += 1
            if not isVisible() and self.label_counter > 1 :
                self.goTrainBTN.setEnabled(True)
            fileName, fileExtension = os.path.splitext(self.image_name)
            image_save_path = join(self.img_save_path, self.image_name)
            database_path = join(self.db_path, fileName + '.csv')

            image_path = join(self.inputFolder, self.image_name)
            cv2.imwrite(image_save_path, cv2.imread(image_path))
            self.operator.writeBboxesToCsv(database_path, self.image_name, self.boxes, self.cvImg.shape[0], self.cvImg.shape[0])

            self.discard_clicked()
        print('accept')

