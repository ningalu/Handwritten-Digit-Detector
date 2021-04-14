import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt

from torchvision import datasets, transforms

from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np

from time import sleep


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.centerWindow()
        self.loadMNIST()
        print(self.train_dataset)
        print(self.test_dataset)

        self.createWidgetLayouts()
        self.createWidgets()
        self.addWidgetsToLayouts()
        self.createCentralLayout()

        self.currImageTableLayout = self.imageTableLayouts[0]

        # Make a field to keep track of the number of images produced
        self.imageCount = 1
        self.newHBox = QtWidgets.QHBoxLayout()

        # Create an iterator of our test dataset
        self.test_it = iter(self.test_dataset)

        # Create a timer with an interval of 1 ms
        self._timer = QtCore.QTimer(self, interval=1)

        # Everytime 1 second is reached , execute the on_timeout function
        self._timer.timeout.connect(self.on_timeout)

        # Start the timer for the first time, it will continue to restart and timeout till we call self._timer.stop()
        self._timer.start()

    def createCentralLayout(self):
        # Make a centralWidget and set it as MainWindow's central widget
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create a Grid Layout where we will assign our two box layouts
        grid = QtWidgets.QGridLayout()
        leftBox = QtWidgets.QVBoxLayout()
        rightBox = QtWidgets.QVBoxLayout()

        # Add required widget layouts to leftBox
        leftBox.addLayout(self.stackedTableLayout)

        # Add required widget layouts to rightBox
        rightBox.addLayout(self.progressBarLayout)

        grid.addLayout(leftBox, 0, 0)
        grid.addLayout(rightBox, 0, 1)

        # Resize columns of grid
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)

        self.centralWidget.setLayout(grid)

    def createWidgetLayouts(self):
        # Create layout for our QStackedLayout that holds all our tables
        self.stackedTableLayout = QtWidgets.QStackedLayout()

        # Create layouts for our scrollAreas
        self.scrollAreaLayouts = []
        for i in range(0, int(len(self.test_dataset) / 500)):
            self.scrollAreaLayouts.append(
                QtWidgets.QScrollArea(widgetResizable=True))

        # Create layouts for our imageTables, and set the content_widget for the imageTables and scrollAreas
        self.imageTableLayouts = []
        for i in range(0, len(self.scrollAreaLayouts)):
            content_widget = QtWidgets.QWidget()
            self.imageTableLayouts.append(
                QtWidgets.QVBoxLayout(content_widget))
            self.scrollAreaLayouts[i].setWidget(content_widget)

        # Create layout for progress bar
        self.progressBarLayout = QtWidgets.QVBoxLayout()

    def createWidgets(self):
        self.progressBar = QtWidgets.QProgressBar()

    def addWidgetsToLayouts(self):
        self.progressBarLayout.addWidget(self.progressBar)

        # Add every scrollAreaLayout to the stackedTableLayout
        for i in range(0, len(self.scrollAreaLayouts)):
            self.stackedTableLayout.addWidget(self.scrollAreaLayouts[i])

    def on_timeout(self):
        try:
            file = next(self.test_it)
            image, label = file
            npImg = image.numpy()[0]
            twod_npImg = (np.reshape(npImg, (28, 28)) * 255).astype(np.uint8)

            PILImg = Image.fromarray(twod_npImg, 'L')
            qimg = ImageQt(PILImg)

            pixmap = QtGui.QPixmap.fromImage(qimg)

            self.add_pixmap(pixmap, label)

        # If the iterator reaches its end, StopIteration is raised, and we can stop our timer
        except StopIteration:
            self._timer.stop()

            sleep(2)
            self.stackedTableLayout.setCurrentIndex(0)
            print("Changed to 0")

        if(self.imageCount % 500) == 0:
            if (self.imageCount < len(self.test_dataset)):
                self._timer.stop()
                print(f'{self.imageCount} images created.')

                # Make the newly finished imageTable visible
                self.stackedTableLayout.setCurrentIndex(
                    int(self.imageCount / 500))

                # Change the currImageTableLayout
                self.currImageTableLayout = self.imageTableLayouts[int(
                    self.imageCount / 500)]

                # Start the timer again
                self._timer.start()
            else:
                print(f'{self.imageCount} images created.')
            # pass

    def add_pixmap(self, pixmap, text):
        if not pixmap.isNull():
            # Our main layout is a HBox with two VBoxes in it
            # This function adds 20 VBoxes each containing an image and their text, to an HBox
            # This HBox is then added to the Left hand side of our main HBox (the scrollArea VBox layout)
            # In this way we simulate creating a table/adding rows (we are just adding HBoxes to a VBox)

            if (self.imageCount % 10 == 0):
                # Add the finished HBox (that has 10 images/texts) to our current imageTableLayout
                self.currImageTableLayout.addLayout(self.newHBox)

                # Remake the HBox to start adding data again
                self.newHBox = QtWidgets.QHBoxLayout()

                # Update our progress bar
                self.progressBar.setValue(
                    int((self.imageCount / (len(self.test_dataset) - 1)) * 100))

            # Create a new VBox to store the current image and label
            imgAndLabelBox = QtWidgets.QVBoxLayout()

            # Create the widgets for our image and label, using the vals the add_pixmap function was passed
            imgLabel = QtWidgets.QLabel(pixmap=pixmap)
            imgLabel.setAlignment(Qt.AlignCenter)
            textLabel = QtWidgets.QLabel(text=str(text))
            textLabel.setAlignment(Qt.AlignCenter)

            # Add the image and text to the VBox
            imgAndLabelBox.addWidget(imgLabel)
            imgAndLabelBox.addWidget(textLabel)

            # Add the VBox to our current HBox (row)
            self.newHBox.addLayout(imgAndLabelBox)

            self.imageCount += 1

    def loadMNIST(self):
        # MNIST Dataset
        self.train_dataset = datasets.MNIST(root='./mnist_data/',
                                            train=True,
                                            transform=transforms.ToTensor(),
                                            download=False)

        self.test_dataset = datasets.MNIST(root='./mnist_data/',
                                           train=False,
                                           transform=transforms.ToTensor())

    def centerWindow(self):
        self.resize(720, 540)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
