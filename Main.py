import sys
from Mainwindow import Mainwindow
from PyQt5.QtWidgets import QApplication


def main():
    a = QApplication(sys.argv)
    w = Mainwindow()
    w.show()
    return a.exec_()


if __name__ == '__main__':
    main()
