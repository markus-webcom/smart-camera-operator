import sys
from seamcarving.Mainwindow import Mainwindow
from PyQt4.QtGui import *


def main():
    a = QApplication(sys.argv)
    w = Mainwindow()
    w.show()
    return a.exec_()


if __name__ == '__main__': main()
