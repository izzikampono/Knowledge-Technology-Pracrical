import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFormLayout


def window():
    app = QApplication(sys.argv)
    win = QWidget()

    e2 = QLineEdit()
    e2.setValidator(QDoubleValidator(0.99, 99.99, 2))

    flo = QFormLayout()
    flo.addRow("Double validator", e2)



    win.setLayout(flo)
    win.setWindowTitle("PyQt")
    win.show()

    sys.exit(app.exec_())


def textchanged(text):
    print("contents of text box: " + text)


def enterPress():
    print("edited")


#if __name__ == '__main__':
    #window()