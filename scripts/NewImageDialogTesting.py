import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt

from torchvision import datasets, transforms

from PIL import Image
from PIL.ImageQt import ImageQt
import io
# import matplotlib.pyplot as plt
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.centerWindow()
        self.loadMNIST()
        print(self.train_dataset)
        print(self.test_dataset)

        # Make a field to keep track of the number of images produced
        self.imageCount = 0
        self.newHBox = QtWidgets.QHBoxLayout()

        # Make a centralWidget and set it as MainWindow's central widget
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        
        # Create layouts for our scroll area and progress bar
        self.scrollAreaLayout = QtWidgets.QVBoxLayout()
        self.progressBarLayout = QtWidgets.QVBoxLayout()

        # Create widgets for scrollArea and progressBar layouts
        self.scrollArea = QtWidgets.QScrollArea(widgetResizable=True)
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setValue(0)

        # Add widgets to our scrollArea and progressBar layouts
        self.scrollAreaLayout.addWidget(self.scrollArea)
        self.progressBarLayout.addWidget(self.progressBar)

        # Add scrollArea and progressBar layouts to our mainHBox layout
        self.mainHBoxLayout = QtWidgets.QHBoxLayout()
        self.mainHBoxLayout.addLayout(self.scrollAreaLayout)
        self.mainHBoxLayout.addLayout(self.progressBarLayout)

        # Self central widget's layout to our mainHBox layout
        self.centralWidget.setLayout(self.mainHBoxLayout)

        # Make a content_widget that stores our image and text layout, add this content_widget to our scrollArea
        content_widget = QtWidgets.QWidget()
        self.imageAndTextLayout = QtWidgets.QVBoxLayout(content_widget)
        self.scrollArea.setWidget(content_widget)

        # Create an iterator of our training dataset
        self.test_it = iter(self.train_dataset)

        # Create a timer with an interval of 1 ms
        self._timer = QtCore.QTimer(self, interval=1)

        # Everytime 1 second is reached , execute the on_timeout function
        self._timer.timeout.connect(self.on_timeout)

        # Start the timer for the first time, it will continue to restart and timeout till we call self._timer.stop()
        self._timer.start()

    def on_timeout(self):
        try:
            file = next(self.test_it)
            image, label = file
            npImg = image.numpy()[0]
            twod_npImg = (np.reshape(npImg, (28,28)) * 255).astype(np.uint8)
            # plt.imshow(twod_npImg)
            # plt.show()

            PILImg = Image.fromarray(twod_npImg, 'L')
            qimg = ImageQt(PILImg)
                
            pixmap = QtGui.QPixmap.fromImage(qimg)

            self.add_pixmap(pixmap, label)

        # If the iterator reaches its end, StopIteration is raised, and we can stop our timer
        except StopIteration:
            self._timer.stop()

    def add_pixmap(self, pixmap, text):
        if not pixmap.isNull():
            # Our main layout is a HBox with two VBoxes in it
            # This function adds 20 VBoxes each containing an image and their text, to an HBox
            # This HBox is then added to the Left hand side of our main HBox (the scrollArea VBox layout)
            # In this way we simulate creating a table/adding rows (we are just adding HBoxes to a VBox)

            if (self.imageCount % 9 == 0):
                # Add the finished HBox (that has 20 images/texts) to our scroll area VBox Layout
                self.imageAndTextLayout.addLayout(self.newHBox)

                # Remake the HBox to start adding data again
                self.newHBox = QtWidgets.QHBoxLayout()

                # Update our progress bar
                self.progressBar.setValue((self.imageCount / len(self.test_dataset) * 100))

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