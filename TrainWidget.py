from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class TrainWidget(QWidget):
    def __init__(self, parent=None,):
        super(TrainWidget, self).__init__(parent)
        self.img_dir=''
        self.operator=None

        self.layout = QVBoxLayout()
        self.TrainBTN = QPushButton('Train Model with new data', self)
        self.returnStartBTN = QPushButton('Startpage', self)
        self.label =QLabel('Successfully Trained')
        self.label.hide()



        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(''))
        hbox.addWidget(self.returnStartBTN)
        hbox.setAlignment(Qt.AlignRight)
        self.layout.setSpacing(50)

        self.layout.addWidget(self.TrainBTN)
        self.layout.addWidget(self.label)
        self.layout.addLayout(hbox)


        self.setLayout(self.layout)

    def setOperator(self,new_operator):
        self.operator=new_operator

    def setTrainDir(self,train_dir):
        self.img_dir=train_dir

    def train_clicked(self):
        print('train')
        print(self.img_dir)
        self.operator.train_model(self.img_dir)
        self.TrainBTN.setEnabled(False)
        self.TrainBTN.hide()
        self.label.show()