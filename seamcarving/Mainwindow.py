from PyQt4.QtCore import QObject, SIGNAL
from seamcarving.Ui import Ui
import numpy as np
from PyQt4.QtGui import *
import cv2 as opencv
from seamcarving.SeamCarver import SeamCarver


class Mainwindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.originalImage = None
        self.columns = 0
        self.rows = 0
        self.imageWithSeams = None
        self.setupUi()
        self.connectButtons()
        self.centerAndRescale()

    def setupUi(self):
        self.ui = Ui(self)
        self.ui.setup()

    def centerAndRescale(self):
        desktop = QDesktopWidget()
        self.move(desktop.availableGeometry(desktop.primaryScreen()).center())
        self.resize(320, 222)

    def connectButtons(self):
        QObject.connect(self.ui.openImageButton, SIGNAL("clicked()"), self.openImageButtonClicked)
        QObject.connect(self.ui.computeSeamsButton, SIGNAL("clicked()"), self.computeSeamButtonClicked)
        QObject.connect(self.ui.removeSeamsButton, SIGNAL("clicked()"), self.removeSeamButtonClicked)
        QObject.connect(self.ui.showOriginalButton, SIGNAL("clicked()"), self.showOriginalButtonClicked)

    def openImageButtonClicked(self):
        self.originalImage = self.readImage(self.requestImagePath())

    def readImage(self, path: str) -> np.array:
        return opencv.imread(path)

    def requestImagePath(self):
        return QFileDialog.getOpenFileName(self, 'Open Image...', '', 'Images *.png *.jpg *.tiff *.tif')

    def computeSeamButtonClicked(self):
        self.columns = self.ui.columnSpinbox.value()
        self.rows = self.ui.rowSpinbox.value()
        self.imageWithSeams = SeamCarver().compute(self.originalImage)
        opencv.imshow("Seam Image:", self.imageWithSeams)

    def removeSeamButtonClicked(self):
        opencv.imshow("Transformed Image:", SeamCarver().remove(self.imageWithSeams))

    def showOriginalButtonClicked(self):
        opencv.imshow("Original Image:", self.originalImage)
