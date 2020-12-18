from imageCompressing import ImageCompressing
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QComboBox, QFileDialog, QLineEdit, QMainWindow
import sys

class GUI(QMainWindow):
    def __init__(self, x, y, width, height, title):
        super(GUI, self).__init__()
        self.imagePath = None
        self.setGeometry(x, y, width, height)
        self.setWindowTitle(title)
        self.initUI()

    def initUI(self):
        self.labelProcessChoiceText = QtWidgets.QLabel(self)
        self.labelProcessChoiceText.setText("Choose image to compress!!!")
        self.labelProcessChoiceText.move(30, 5)
        self.labelProcessChoiceText.resize(160, 20)

        self.buttonGetimagePath = QtWidgets.QPushButton(self)
        self.buttonGetimagePath.setText("Choose Image!")
        self.buttonGetimagePath.move(0, 30)
        self.buttonGetimagePath.resize(200, 40)
        self.buttonGetimagePath.clicked.connect(self.buttonGetimagePathIsClicked)

        self.labelImagePath = QtWidgets.QLabel(self)
        self.labelImagePath.setText("Image Path: ")
        self.labelImagePath.move(5, 80)
        self.labelImagePath.resize(160, 20)
        
        self.labelImagePathValue = QtWidgets.QLabel(self)
        self.labelImagePathValue.setText(str(self.imagePath))
        self.labelImagePathValue.move(70, 80)
        self.labelImagePathValue.resize(300, 20)
        self.labelImagePathValue.setEnabled(False)

        self.comboBox = QComboBox(self)
        self.comboBox.move(200, 200)
        self.comboBox.resize(200, 20)

        self.comboBoxData = QComboBox(self)
        self.comboBoxData.move(0, 200)
        self.comboBoxData.resize(100, 20)

    def buttonGetimagePathIsClicked(self):
        self.imagePath = QFileDialog.getOpenFileName()[0]
        self.buttonGetimagePath.setEnabled(False)
        self.labelImagePathValue.setEnabled(True)
        self.labelImagePathValue.setText(str(self.imagePath))
        sample = ImageCompressing(self.imagePath)
        for i in range(len(sample.orderedValues[0])):
            self.comboBox.addItem("Value: " + str(sample.orderedValues[0][i]) + " Freq: " + str(sample.orderedValues[1][i]))
        for i in sample.convertedArray:
            self.comboBoxData.addItem(str(i))
        
app = QApplication(sys.argv)
win = GUI(200, 200, 400, 400, "Image Compressing")
win.show()
sys.exit(app.exec_())