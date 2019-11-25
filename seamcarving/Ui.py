from PyQt4.QtGui import *


class Ui:
    def __init__(self, parent):
        self.parent = parent

    def setup(self):
        self.mainPanel = QWidget(self.parent)
        self.mainPanel.setLayout(QVBoxLayout())
        self.parent.setCentralWidget(self.mainPanel)
        self.openImageButton = QPushButton(self.parent)
        self.openImageButton.setText("Load Image")
        self.mainPanel.layout().addWidget(self.openImageButton)
        self.panel0 = QWidget(self.parent)
        self.panel0.setLayout(QHBoxLayout())
        self.mainPanel.layout().addWidget(self.panel0)
        self.label1 = QLabel(self.parent)
        self.label1.setText("Cols")
        self.panel0.layout().addWidget(self.label1)
        self.label2 = QLabel(self.parent)
        self.label2.setText("Rows")
        self.panel0.layout().addWidget(self.label2)
        self.panel1 = QWidget(self.parent)
        self.panel1.setLayout(QHBoxLayout())
        self.mainPanel.layout().addWidget(self.panel1)
        self.columnSpinbox = QSpinBox(self.parent)
        self.panel1.layout().addWidget(self.columnSpinbox)
        self.rowSpinbox = QSpinBox(self.parent)
        self.panel1.layout().addWidget(self.rowSpinbox)
        self.computeSeamsButton = QPushButton(self.parent)
        self.computeSeamsButton.setText("Compute Seams")
        self.mainPanel.layout().addWidget(self.computeSeamsButton)
        self.removeSeamsButton = QPushButton(self.parent)
        self.removeSeamsButton.setText("Remove Seams")
        self.mainPanel.layout().addWidget(self.removeSeamsButton)
        self.showOriginalButton = QPushButton(self.parent)
        self.showOriginalButton.setText("Show Original")
        self.mainPanel.layout().addWidget(self.showOriginalButton)


