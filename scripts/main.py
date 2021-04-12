import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QDesktopWidget, qApp, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMenuBar, QPushButton, QLabel, QLineEdit, QFrame
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

import cv2
import torch
import numpy as np
from PIL import Image

from os import makedirs, path

from TrainingDialog import TrainingDialog
from ViewImagesDialog import ViewImagesDialog
from Net import Net


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.trainingDialog = 0
        self.viewTrainImagesDialog = 0
        self.viewTestImagesDialog = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Handwritten Digit Recognizer')

        self.createWidgetLayouts()
        self.createCentralLayout()
        self.createMenuBar()
        self.centreWindow()
        self.show()

    def centreWindow(self):
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())
        self.resize(720, 540)

    def createMenuBar(self):
        # Create Actions
        trainModelAct = QAction('&Train Model', self)
        trainModelAct.triggered.connect(self.showTrainingDialog)
        exitAct = QAction('&Quit', self)
        exitAct.triggered.connect(qApp.quit)

        viewTrainImgsAct = QAction('&View Training Images', self)
        viewTrainImgsAct.triggered.connect(self.showTrainImagesDialog)
        viewTestImgsAct = QAction('&View Testing Images', self)
        viewTestImgsAct.triggered.connect(self.showTestImagesDialog)

        # Create MenuBar
        menubar = self.menuBar()

        # Add menus and actions to the MenuBar
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(trainModelAct)
        fileMenu.addAction(exitAct)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(viewTrainImgsAct)
        viewMenu.addAction(viewTestImgsAct)

    def createCentralLayout(self):
        # Create a central QWidget that can be displayed in QMainWindow
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create a Grid Layout where we will assign our two box layouts
        grid = QGridLayout()
        leftBox = QVBoxLayout()
        rightBox = QVBoxLayout()

        # Add required widget layouts to leftBox
        leftBox.addLayout(self.canvasLayout)

        # Add required widget layouts to rightBox
        rightBox.addLayout(self.buttonLayout)
        rightBox.addLayout(self.classProbLayout)

        # Add left and right boxes (containing our widget layouts) to grid
        grid.addLayout(leftBox, 0, 0)
        grid.addLayout(rightBox, 0, 1)

        # Resize columns of grid
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)

        #Set central widget's layout to our grid
        self.centralWidget.setLayout(grid)

    def mouseMoveEvent(self, e):
        painter = QtGui.QPainter(self.canvas.pixmap())
        p = painter.pen()
        p.setWidth(20)
        p.setCapStyle(0x20)

        painter.setPen(p)
        painter.drawPoint(e.x()-self.canvas.pos().x(), e.y() -
                          self.canvas.pos().y()-self.menuBar().frameSize().height())
        #print(self.canvas.pos().x(), self.canvas.pos().y())
        #print(e.x(), e.y())
        painter.end()
        self.update()

    def createWidgetLayouts(self):
        # -- Creating Left Side of Layout
        # Create a box layout for the canvas
        self.canvasLayout = QVBoxLayout()
        # Create canvas widget
        self.canvas = QFrame(self).heightForWidth(self.height())
        self.canvas = QtWidgets.QLabel()
        self.canvas_size = QtCore.QSize(self.canvas.height() + self.menuBar().frameSize().height(), 
            self.canvas.height() + self.menuBar().frameSize().height())
        canvas_content = QtGui.QPixmap(self.canvas_size)

        canvas_content.fill(QtGui.QColor("white"))
        self.canvas.setPixmap(canvas_content)
        #self.canvas.setStyleSheet(
        #    "QWidget { border: 2px solid cornflowerblue; background-color: white;}")
        #Add canvas widget to canvas layout
        self.canvasLayout.addWidget(self.canvas)

        # -- Creating Right Side of Layout
        # Create a buttonLayout (a vbox)
        self.buttonLayout = QVBoxLayout()
        # Style buttons
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)

        # Create buttons
        self.clearButton = QPushButton('Clear')
        self.clearButton.setShortcut('Ctrl+Z')
        self.clearButton.clicked.connect(self.clear)
        self.randomButton = QPushButton('Random')
        # self.randomButton.clicked.connect()
        self.modelButton = QPushButton('Model')
        # self.modelButton.clicked.connect()
        self.recognizeButton = QPushButton('Recognize')
        self.recognizeButton.setShortcut('Ctrl+R')
        self.recognizeButton.clicked.connect(self.recognize)
        self.saveButton = QPushButton('Save')
        self.saveButton.setShortcut('Ctrl+S')
        self.saveButton.clicked.connect(lambda: self.save(True))

        # Add buttons to the box
        self.buttonLayout.addWidget(self.clearButton)
        self.buttonLayout.addWidget(self.randomButton)
        self.buttonLayout.addWidget(self.modelButton)
        self.buttonLayout.addWidget(self.recognizeButton)
        self.buttonLayout.addWidget(self.saveButton)

        # Create a layout for the class probability display
        self.classProbLayout = QVBoxLayout()

        # Create widgets for probability display
        self.classGraphLabel = QLabel('Class Probability')
        self.classGraphLabel.setAlignment(Qt.AlignCenter)

        self.classGraph = QLineEdit('Graph of class probability')
        
        self.classDetected = QLineEdit('Class detected')
        self.classDetected.setReadOnly(True)
        self.classDetected.setAlignment(Qt.AlignCenter)

        # Add widgets to the box
        self.classProbLayout.addWidget(self.classGraphLabel)
        self.classProbLayout.addWidget(self.classGraph)
        self.classProbLayout.addWidget(self.classDetected)

    def showTrainingDialog(self):
        self.trainingDialog = TrainingDialog()
        self.trainingDialog.exec_()
        print(self.trainingDialog.model)

    def showTrainImagesDialog(self):
        try:  # Check if the dataset has been acquired by the trainingDialog yet
            self.train_dataset = self.trainingDialog.getTrainSet()

            if len(self.train_dataset) == 0:
                raise AttributeError
        except AttributeError:  # If not let the user know they have to get the dataset before viewing images
            dataMissingDialog = QMessageBox()
            dataMissingDialog.setWindowTitle('Data Missing')
            dataMissingDialog.setIcon(QMessageBox.Critical)
            dataMissingDialog.setText("The training dataset is missing.")
            dataMissingDialog.setInformativeText(
                "Make sure you go to File > Train Model and click 'Download MNIST' first.")

            dataMissingDialog.exec_()
        else:  # Otherwise create and execute the ViewImagesDialog
            self.viewTrainImagesDialog = ViewImagesDialog(
                'View Training Images', self.train_dataset)
            self.viewTrainImagesDialog.exec_()

    def showTestImagesDialog(self):
        try:  # Check if the dataset has been acquired by the trainingDialog yet
            self.test_dataset = self.trainingDialog.getTestSet()

            if len(self.test_dataset) == 0:
                raise AttributeError
        except AttributeError:  # If not let the user know they have to get the dataset before viewing images
            dataMissingDialog = QMessageBox()
            dataMissingDialog.setWindowTitle('Data Missing')
            dataMissingDialog.setIcon(QMessageBox.Critical)
            dataMissingDialog.setText("The test dataset is missing.")
            dataMissingDialog.setInformativeText(
                "Make sure you go to File > Train Model and click 'Download MNIST' first.")

            dataMissingDialog.exec_()
        else:  # Otherwise create and execute the ViewImagesDialog
            self.viewTrainImagesDialog = ViewImagesDialog(
                'View Test Images', self.test_dataset)
            self.viewTrainImagesDialog.exec_()

    def clear(self):
        clear_canvas = QtGui.QPixmap(self.canvas.pixmap().size())
        clear_canvas.fill(QtGui.QColor("white"))
        self.canvas.setPixmap(clear_canvas)

    def recognize(self):
        self.save(False)
        
        # model = self.trainingDialog.model.eval()
        # if self.trainingDialog != []:
        #     model = self.trainingDialog.model.eval()
        # else:
        #     model = Net()
        #     model.load_state_dict(torch.load(./))

        model = Net()
        model.load_state_dict(torch.load('./mnist_model.zip'))
        model.eval()

        # img = cv2.imread('./images/user_drawing.png', cv2.IMREAD_GRAYSCALE)
        # img = cv2.resize(img, (28,28))
        
        img = Image.open('./images/user_drawing.png')
        img = img.resize((28, 28))
        img = img.convert('L')
        img = np.invert(img)
        img = np.split(img, 28)
        img = np.array(img)

        #img = img / 255
        #img = np.array(img)
        # img = img.astype('float32')
        # img = img.reshape(1, 28, 28, 1)
        # img = 255-img
        # img /= 255

        output = model(torch.Tensor(img))
        print(output)
        prediction = torch.argmax(output)
        print(prediction.item())
        self.classDetected.setText(str(prediction.item()))

    def save(self, showDialog: bool):
        imgPath = './images/user_drawing.png'

        if not path.exists(imgPath):
            makedirs(imgPath)

        self.canvas.pixmap().save(imgPath)

        if (showDialog):
            imageSavedDialog = QMessageBox()
            imageSavedDialog.setWindowTitle('Image saved')
            imageSavedDialog.setIcon(QMessageBox.Information)
            imageSavedDialog.setText(f'Your drawing has been saved to "{imgPath}"')

            imageSavedDialog.exec_()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   sys.exit(app.exec_())
