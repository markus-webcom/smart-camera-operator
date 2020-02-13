import sys
import cv2

#from PyQt5.QtGui import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class ConvertWidget(QWidget):
    def __init__(self, parent=None):
        super(ConvertWidget, self).__init__(parent)

        self.ratio_x = 0
        self.ratio_y = 0
        self.width = 0
        self.height=0

        self.selectedRatioX=0
        self.selectedRatioY=0


        self.ConvertPreciseBTN = QPushButton('Convert precise for each frame', self)
        self.ConvertQuickBTN = QPushButton('Convert with interpolation', self)
        self.ChooseFileBTN=QPushButton('Choose Video File',self)
        self.returnStartBTN=QPushButton('Startpage',self)

        self.ratioInLabel=QLabel('Input ratio: :')
        self.ratioOutLabel=QLabel('Output ratio: :')
        self.ratioInputLabel = QLabel('')
        self.ratioInLabel.setFixedHeight(20)
        self.ratioOutLabel.setFixedHeight(20)
        self.ratioInputLabel.setFixedHeight(20)

        self.ratioCBox=QComboBox(self)
        self.ratioCBox.activated[str].connect(self.onChangedCBox)


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

        hbox2=QHBoxLayout()
        hbox2.addWidget(self.ratioInLabel)
        hbox2.addWidget(self.ratioOutLabel)
        hbox3=QHBoxLayout()
        hbox3.addWidget(self.ratioInputLabel)
        hbox3.addWidget(self.ratioCBox)

        layout.addWidget(self.ChooseFileBTN)
        layout.addLayout(hbox2)
        layout.addLayout(hbox3)

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
            self.operator.convertQuickVideo(self.inputFile,self.progressBar,self.selectedRatioX,self.selectedRatioY)
            self.progressBar.hide()

    def convertPreciseClicked(self):
        if self.inputFile is not None:
            self.operator.convertPreciseVideo(self.inputFile,self.progressBar,self.selectedRatioX,self.selectedRatioY)
            self.progressBar.hide()


    def chooseFileClicked(self):
        self.inputFile = QFileDialog.getOpenFileName(self, 'Open video(mp4)...', '', 'Video Files (*.mp4)')[0]
        self.setInputRatio()
        currentRatio=self.ratioCBox.currentText()
        currentRatio=currentRatio.split(':')
        self.selectedRatioX=int(currentRatio[0])
        self.selectedRatioY=int(currentRatio[1])
        print(self.selectedRatioX,self.selectedRatioY)


    def onChangedCBox(self,text):
        currentRatio = text.split(':')
        self.selectedRatioX = int(currentRatio[0])
        self.selectedRatioY = int(currentRatio[1])
        print(self.selectedRatioX, self.selectedRatioY)


    def setInputRatio(self):
        vcap = cv2.VideoCapture(self.inputFile)
        self.width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ratio=self.calculate_ratio(self.height,self.width)
        self.ratioInputLabel.setText( ratio)
        self.matchingVideoFormat()


    def calculate_ratio(self,width, height):
        temp = 0

        def gcd(a, b):
            #greatest common divisor
            return a if b == 0 else gcd(b, a % b)

        if width == height:
            return "1:1"

        if width < height:
            temp = width
            width = height
            height = temp

        divisor = gcd(width, height)

        x = int(width / divisor) if not temp else int(height / divisor)
        y = int(height / divisor) if not temp else int(width / divisor)
        self.ratio_x=x
        self.ratio_y=y

        return f"{y}:{x}"

    def matchingVideoFormat(self):
        inputRatio=(self.width,self.height)
        print(inputRatio)
        if self.ratio_x==9 and self.ratio_y==16:
            formats=[(426, 240),(640 , 360),(854, 480),(1280, 720),(1920 ,1080),(2560,1440),(3840 , 2160)]
            if not (inputRatio in formats):
                formats.insert(0,formats)

            self.setFormatOptions(formats)

            print('16:9')
        elif self.ratio_x==3 and self.ratio_y==4:
            formats = [(1280, 960),(1920 , 1440)]
            if not (inputRatio in formats):
                formats.insert(0, formats)
            self.setFormatOptions(formats)
            print('4:3')
        else:
            formats=[inputRatio]
            self.setFormatOptions(formats)
            print('else')

    def setFormatOptions(self,formats):
        for f in formats:
            item=f"{f[1]}:{f[0]}"
            self.ratioCBox.addItem(item)



