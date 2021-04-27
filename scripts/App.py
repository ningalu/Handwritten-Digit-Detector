from os import makedirs, path
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QDesktopWidget, qApp, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMenuBar, QPushButton, QLabel, QLineEdit, QFrame
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

import torch
import numpy as np
from PIL import Image

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from TrainingDialog import TrainingDialog
from ViewImagesDialog import ViewImagesDialog
from ModelSelectDialog import ModelSelectDialog
from Net import Net


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selectedModel = 'None'

        self.trainingDialog = 0
        self.modelSelectDialog = 0
        self.viewTrainImagesDialog = 0
        self.viewTestImagesDialog = 0

        if (path.exists('./mnist_model.zip')):
            self.selectModel('PyTorch')

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Handwritten Digit Recognizer')
        
        self.createWidgetLayouts()
        self.createCentralLayout()
        self.createMenuBar()
        self.centreWindow()
        self.show()

    def centreWindow(self):

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
        p.setWidth(35)
        p.setCapStyle(0x20)
        
        painter.setPen(p)
        painter.drawPoint(e.x()-self.canvas.pos().x(), e.y()-self.canvas.pos().y()-self.menuBar().frameSize().height())
        painter.end()
        self.update()

    def clear(self):
        clear_canvas = QtGui.QPixmap(self.canvas.pixmap().size())
        clear_canvas.fill(QtGui.QColor("white"))
        self.canvas.setPixmap(clear_canvas)

    def createWidgetLayouts(self):
        # -- Creating Left Side of Layout
        # Create a box layout for the canvas
        self.canvasLayout = QVBoxLayout()

        # Create canvas widget
        self.canvas = QFrame(self).heightForWidth(self.height())
        self.canvas = QtWidgets.QLabel()
        self.canvas_size = QtCore.QSize(self.canvas.height() + self.menuBar().frameSize().height(), self.canvas.height() + self.menuBar().frameSize().height())
        canvas_content = QtGui.QPixmap(self.canvas_size)
        canvas_content.fill(QtGui.QColor("white"))
        self.canvas.setPixmap(canvas_content)

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
        self.clearButton.setShortcut('Ctrl+C')
        self.clearButton.clicked.connect(self.clear)
        self.modelButton = QPushButton('Model')
        self.modelButton.setShortcut('Ctrl+M')
        self.modelButton.clicked.connect(self.model)
        self.recognizeButton = QPushButton('Recognize')
        self.recognizeButton.setShortcut('Ctrl+R')
        self.recognizeButton.clicked.connect(self.recognize)
        self.saveButton = QPushButton('Save')
        self.saveButton.setShortcut('Ctrl+S')
        self.saveButton.clicked.connect(lambda: self.save(True))

        # Add buttons to the box
        self.buttonLayout.addWidget(self.clearButton)
        self.buttonLayout.addWidget(self.modelButton)
        self.buttonLayout.addWidget(self.recognizeButton)
        self.buttonLayout.addWidget(self.saveButton)

        # Create a layout for the class probability display
        self.classProbLayout = QVBoxLayout()

        # Create class probability widgets
        self.classGraphLabel = QLabel('Class Probability')
        self.classGraphLabel.setAlignment(Qt.AlignCenter)

        self.initPlot()

        self.classGraph = QLineEdit('Graph of class probability')
        
        self.classDetectedLine = QLineEdit('Class detected')
        self.classDetectedLine.setReadOnly(True)
        self.classDetectedLine.setAlignment(Qt.AlignCenter)

        # Add widgets to the box
        self.classProbLayout.addWidget(self.classGraphLabel)
        self.classProbLayout.addWidget(self.graph)
        self.classProbLayout.addWidget(self.classDetectedLine)

    def initPlot(self):
        self.figure = plt.figure()
        self.graph = FigureCanvas(self.figure)
        self.plotList([0]*10)

    def plotList(self, prob_list):
        self.figure.clear()
        prob_list = [0 if i < 0 else i for i in prob_list]
        ax = self.figure.add_subplot(111)
        ax.barh(list(range(0, 10)), prob_list)
        ax.set_yticks(list(range(0, 10)))
        ax.set_xticks([])
        self.graph.draw()

    def showTrainingDialog(self):
        self.trainingDialog = TrainingDialog()
        self.trainingDialog.trainingFinished.connect(self.selectModel)
        self.trainingDialog.exec_()

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

    def showModelSelectDialog(self):
        self.modelSelectDialog = ModelSelectDialog(self.selectedModel)
        self.modelSelectDialog.modelSelected.connect(self.selectModel)
        self.modelSelectDialog.exec_()
    
    def selectModel(self, model: str):
        self.selectedModel = model

    def clear(self):
        clear_canvas = QtGui.QPixmap(self.canvas.pixmap().size())
        clear_canvas.fill(QtGui.QColor("white"))
        self.canvas.setPixmap(clear_canvas)

    def model(self):
        self.showModelSelectDialog()

    def recognize(self):
        self.save(False)

        if (self.selectedModel == 'PyTorch'):
            if path.exists('./mnist_model.zip'):
                model = Net()
                model.load_state_dict(torch.load('./mnist_model.zip'))
                model.eval()

                # Open the image the user drew, resize it to 28,28
                img = Image.open('./images/user_drawing.png', 'r')
                img = img.resize((28, 28), Image.ANTIALIAS)

                # Convert the image to greyscale, then to a nparray, the invert it's colour (to be white on black)
                img = img.convert('L')
                img = np.array(img)
                img = np.invert(img)

                # Save how img currently looks (store it in the variable gimg)
                gimg = Image.fromarray(img, 'L')
                gimg.save('./images/user_drawing_inverted.png')

                # Get the dimensions of the img array
                numRows, numCols = img.shape

                # Find the rows and cols of img that contain only zeros
                zeroRows = []
                for row in range(0, numRows - 1):
                    if (not np.count_nonzero(img[row,:])):
                        zeroRows.append(row)

                zeroCols = []
                for col in range(0, numCols):
                    if (not np.count_nonzero(img[:,col])):
                        zeroCols.append(col)

                if (len(zeroCols) < 18):
                    # Delete the rows and cols that are only zeros
                    img = np.delete(img, tuple(zeroRows), axis = 0)
                    img = np.delete(img, tuple(zeroCols), axis = 1)
                else: # If there are a large amount of zero cols we should not remove them as the image would be too small for processing
                    img = np.delete(img, tuple(zeroRows), axis = 0)

                # Save how img looks after removing black borders
                gimg = Image.fromarray(img, 'L')
                gimg.save('./images/user_drawing_zeros_removed.png')

                # Resize image to 20,20
                img = Image.fromarray(img, 'L')
                img = img.resize((20,20), Image.ANTIALIAS)
                img.save('./images/user_drawing_zeros_removed_20.png')

                # Create a blank 28,28 black image
                newImg = Image.new('L', (28,28))

                # Paste the 20,20 in the center to make the completed 28,28
                newImg.paste(img, (4,4))
                newImg.save('./images/input_image.png')

                # Convert back to np array
                newImg = np.array(newImg)

                output = model(torch.Tensor(newImg))
                # print(output)

                self.plotList(output.tolist()[0])

                prediction = torch.argmax(output)
                print(f'Digit {prediction.item()} predicted')
                self.classDetectedLine.setText(str(prediction.item()))

            else:
                imageSavedDialog = QMessageBox()
                imageSavedDialog.setWindowTitle('PyTorch model missing')
                imageSavedDialog.setIcon(QMessageBox.Critical)
                imageSavedDialog.setText("To use this model you must first train it by going to File > Train Model and clicking 'Train'")

                imageSavedDialog.exec_()

        elif (self.selectedModel == 'None'):
            noModelDialog = QMessageBox()
            noModelDialog.setWindowTitle('No model selected')
            noModelDialog.setIcon(QMessageBox.Information)
            noModelDialog.setText("You must select a model by clicking on the 'Model' button on the main screen")

            noModelDialog.exec_()

    def save(self, showDialog: bool):

        if not path.exists('./images/'):
            makedirs('./images')
            img = Image.new('L', (510,510))
            img.save("./images/user_drawing.png", "png")

        self.canvas.pixmap().save(f"./images/user_drawing.png")

        if (showDialog):
            imageSavedDialog = QMessageBox()
            imageSavedDialog.setWindowTitle('Image saved')
            imageSavedDialog.setIcon(QMessageBox.Information)
            imageSavedDialog.setText(f'Your drawing has been saved to "./images/user_drawing.png"')

            imageSavedDialog.exec_()
