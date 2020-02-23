from os.path import join
import os

#from PyQt5.QtGui import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtWidgets import *
from StartWidget import StartWidget
from LabelWidget import LabelWidget
from ConvertWidget import ConvertWidget
from Operator import Operator
from TrainWidget import TrainWidget
from LabelImagesWidget import LabelImagesWidget
from LabelVideoWidget import LabelVideoWidget






class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(150, 150, 400, 450)
        self.setFixedSize(2500, 1700)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.showStartWidget()
        self.widgetData=None
        self.operator=Operator()
        self.setStyleSheet(open('style.css').read())

    def showConvertWidget(self):
        convert_widget = ConvertWidget(self)
        convert_widget.returnStartBTN.clicked.connect(self.showStartWidget)
        self.central_widget.addWidget(convert_widget)
        self.central_widget.setCurrentWidget(convert_widget)
        self.setWindowTitle("ConvertWindow")
        convert_widget.setOperator(self.operator)

    def showLabelWidget(self):
        label_widget = LabelWidget(self)
        label_widget.LabelImagesBTN.clicked.connect(self.showLabelImagesWidget)
        label_widget.LabelVideoBTN.clicked.connect(self.showLabelVideoWidget)
        label_widget.returnStartBTN.clicked.connect(self.showStartWidget)
        self.central_widget.addWidget(label_widget)
        self.central_widget.setCurrentWidget(label_widget)
        self.setWindowTitle("LabelWindow")

    def showLabelImagesWidget(self):
        label_widget = LabelImagesWidget(self)
        label_widget.goTrainBTN.clicked.connect(self.showTrainWidget)
        label_widget.returnStartBTN.clicked.connect(self.showStartWidget)
        label_widget.setOperator(self.operator)
        self.central_widget.addWidget(label_widget)
        self.central_widget.setCurrentWidget(label_widget)
        self.setWindowTitle("LabelImagesWindow")
        self.widgetData=label_widget

    def showLabelVideoWidget(self):
        label_widget=LabelVideoWidget(self)
        label_widget.goTrainBTN.clicked.connect(self.showTrainWidget)
        label_widget.returnStartBTN.clicked.connect(self.showStartWidget)
        label_widget.setOperator(self.operator)
        self.central_widget.addWidget(label_widget)
        self.central_widget.setCurrentWidget(label_widget)
        self.setWindowTitle("LabelImagesWindow")
        self.widgetData = label_widget

    def showStartWidget(self):
        start_widget = StartWidget(self)
        start_widget.LabelBTN.clicked.connect(self.showLabelWidget)
        start_widget.ConvertBTN.clicked.connect(self.showConvertWidget)
        self.central_widget.addWidget(start_widget)
        self.central_widget.setCurrentWidget(start_widget)
        self.setWindowTitle("StartWindow")

    def showTrainWidget(self):
        train_dir=self.widgetData.getTrainDir()
        print(train_dir)
        train_widget = TrainWidget(self)
        train_widget.setTrainDir(train_dir)
        train_widget.TrainBTN.clicked.connect(train_widget.train_clicked)
        train_widget.returnStartBTN.clicked.connect(self.showStartWidget)
        train_widget.setOperator(self.operator)
        self.central_widget.addWidget(train_widget)
        self.central_widget.setCurrentWidget(train_widget)
        self.setWindowTitle("TrainWindow")








