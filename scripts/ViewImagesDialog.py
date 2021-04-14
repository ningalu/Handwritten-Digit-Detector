import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QStackedLayout
from PyQt5.QtWidgets import QWidget, QScrollArea, QProgressBar, QLabel, QPushButton, QCheckBox, QFrame
from PyQt5.QtCore import Qt

from torchvision import datasets, transforms

from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np


class ViewImagesDialog(QDialog):
    def __init__(self, title, dataset):
        super().__init__()
        self.dataset = dataset
        self.title = title

        self.initUI()
        self.currImageTableLayout = self.imageTableLayouts[0]

        # Make a field to keep track of the number of images produced
        self.imageCount = 1
        self.newHBox = QHBoxLayout()

        # Create an iterator of our dataset
        self.dataset_it = iter(self.dataset)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.centerWindow()

        self.createWidgetLayouts()
        self.createWidgets()
        self.addWidgetsToWidgetLayouts()
        self.createCentralLayout()

    def centerWindow(self):
        self.resize(720, 540)

    def createWidgetLayouts(self):
        # Create layout for our QStackedLayout that holds all our tables
        self.stackedTableLayout = QStackedLayout()

        # Create layouts for our scrollAreas
        self.scrollAreaLayouts = []
        for i in range(0, int(len(self.dataset) / 500)):
            self.scrollAreaLayouts.append(
                QScrollArea(widgetResizable=True))

        # Create layouts for our imageTables, and set the content_widget for the imageTables and scrollAreas
        self.imageTableLayouts = []
        for i in range(0, len(self.scrollAreaLayouts)):
            content_widget = QWidget()
            self.imageTableLayouts.append(
                QVBoxLayout(content_widget))
            self.scrollAreaLayouts[i].setWidget(content_widget)

        # Create layout to hold the filter and progress layouts
        self.filterAndProgressLayout = QVBoxLayout()

        # Create filter layout
        self.filterLabelLayout = QHBoxLayout()

        self.checkBoxLayoutOne = QHBoxLayout()
        self.checkBoxLayoutTwo = QHBoxLayout()

        self.filterLayout = QVBoxLayout()
        self.filterLayout.addLayout(self.filterLabelLayout)
        self.filterLayout.addLayout(self.checkBoxLayoutOne)
        self.filterLayout.addLayout(self.checkBoxLayoutTwo)
        self.filterLayout.setAlignment(Qt.AlignTop)

        # Create layout for progress bar and run button
        self.progressLayout = QHBoxLayout()
        self.progressLayout.setAlignment(Qt.AlignTop)

        # Create layout for nav buttons and the general nav layout
        self.navButtonLayout = QHBoxLayout()
        self.tableNumberLabelLayout = QVBoxLayout()
        self.navLayout = QVBoxLayout()
        self.navLayout.setAlignment(Qt.AlignBottom)

    def createWidgets(self):
        # Filter label and checkboxes
        self.filterLabel = QLabel('Filters:')

        self.checkBoxes = [] 
        for i in range(0, 11):
            self.checkBoxes.append(QCheckBox(str(i)))

        # Progress Bar and run button
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        self.loadButton = QPushButton('Load')
        self.loadButton.clicked.connect(self.loadImages)

        # Nav Buttons (should be disabled till the timer stops) and tableNumberLabel
        self.prevButton = QPushButton('Previous')
        self.prevButton.clicked.connect(
            lambda: self.setStackedTableIndex('prev'))
        self.prevButton.setDisabled(True)
        self.nextButton = QPushButton('Next')
        self.nextButton.clicked.connect(
            lambda: self.setStackedTableIndex('next'))
        self.nextButton.setDisabled(True)

        self.tableNumberLabel = QLabel('')
        self.tableNumberLabel.setAlignment(Qt.AlignCenter)

    def addWidgetsToWidgetLayouts(self):
        # Add every scrollAreaLayout to the stackedTableLayout
        for i in range(0, len(self.scrollAreaLayouts)):
            self.stackedTableLayout.addWidget(self.scrollAreaLayouts[i])

        # Add filter label and checkboxes
        self.filterLabelLayout.addWidget(self.filterLabel)
        for i in range(0, 5):
            self.checkBoxLayoutOne.addWidget(self.checkBoxes[i])
            self.checkBoxLayoutTwo.addWidget(self.checkBoxes[i + 5])

        # Add progress bar and load button
        self.progressLayout.addWidget(self.loadButton)
        self.progressLayout.addWidget(self.progressBar)

        # Add nav buttons and tableNumberLabel
        self.navButtonLayout.addWidget(self.prevButton)
        self.navButtonLayout.addWidget(self.nextButton)
        self.tableNumberLabelLayout.addWidget(self.tableNumberLabel)

        self.navLayout.addLayout(self.navButtonLayout)
        self.navLayout.addLayout(self.tableNumberLabelLayout)

        self.filterAndProgressLayout.addLayout(self.filterLayout)
        self.filterAndProgressLayout.addLayout(self.progressLayout)

    def createCentralLayout(self):
        # Create a Grid Layout where we will assign our two box layouts
        grid = QGridLayout()
        leftBox = QVBoxLayout()
        rightBox = QVBoxLayout()

        # Add required widget layouts to leftBox
        leftBox.addLayout(self.stackedTableLayout)

        # Add required widget layouts to rightBox
        rightBox.addLayout(self.filterAndProgressLayout)
        rightBox.addLayout(self.navLayout)

        grid.addLayout(leftBox, 0, 0)
        grid.addLayout(rightBox, 0, 1)

        # Resize columns of grid
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 1)

        self.setLayout(grid)

    def loadImages(self):
        # Create a timer with an interval of 0s (as soon as it can timeout)
        self.timer = QtCore.QTimer(self, interval=0)

        # Everytime 1 second is reached , execute the onTimeout function
        self.timer.timeout.connect(self.onTimeout)

        # Start the timer for the first time, it will continue to restart and timeout till we call self.timer.stop()
        self.timer.start()

    def onTimeout(self):
        try:
            file = next(self.dataset_it)
            image, label = file
            npImg = image.numpy()[0]
            twod_npImg = (np.reshape(npImg, (28, 28)) * 255).astype(np.uint8)

            PILImg = Image.fromarray(twod_npImg, 'L')
            qimg = ImageQt(PILImg)

            pixmap = QtGui.QPixmap.fromImage(qimg)

            self.addPixmap(pixmap, label)

        # If the iterator reaches its end, StopIteration is raised, and we can stop our timer
        except StopIteration:
            self.timer.stop()

            # We can now let the user click the nav buttons
            self.prevButton.setDisabled(False)
            self.nextButton.setDisabled(False)
            # Roll back to the first page
            self.stackedTableLayout.setCurrentIndex(0)
            # And set the page number
            self.setTableNumberLabel()

        if(self.imageCount % 500) == 0:
            if (self.imageCount < len(self.dataset)):
                self.timer.stop()
                print(f'{self.imageCount} images created.')

                # Make the newly finished imageTable visible
                self.stackedTableLayout.setCurrentIndex(
                    int(self.imageCount / 500))

                # Change the currImageTableLayout
                self.currImageTableLayout = self.imageTableLayouts[int(
                    self.imageCount / 500)]

                # Start the timer again
                self.timer.start()
            else:
                print(f'{self.imageCount} images created.')

    def addPixmap(self, pixmap, text):
        if not pixmap.isNull():
            # This function adds 10 VBoxes each containing an image and their text, to an HBox
            # This HBox is then added to the scrollArea Vbox in the Right hand side of our main grid
            # In this way we simulate creating a table/adding rows (we are just adding HBoxes to a VBox)

            if (self.imageCount % 10 == 0):
                # Add the finished HBox (that has 10 images/texts) to our current imageTableLayout
                self.currImageTableLayout.addLayout(self.newHBox)

                # Remake the HBox to start adding data again
                self.newHBox = QHBoxLayout()

                # Update our progress bar
                self.progressBar.setValue(
                    int((self.imageCount / (len(self.dataset) - 1)) * 100))

            # Create a new VBox to store the current image and label
            imgAndLabelBox = QVBoxLayout()

            # Create the widgets for our image and label, using the vals the add_pixmap function was passed
            imgLabel = QLabel(pixmap=pixmap)
            imgLabel.setAlignment(Qt.AlignCenter)
            textLabel = QLabel(text=str(text))
            textLabel.setAlignment(Qt.AlignCenter)

            # Add the image and text to the VBox
            imgAndLabelBox.addWidget(imgLabel)
            imgAndLabelBox.addWidget(textLabel)

            # Add the VBox to our current HBox (row)
            self.newHBox.addLayout(imgAndLabelBox)

            self.imageCount += 1

    def setStackedTableIndex(self, index: str):
        currTable = self.stackedTableLayout.currentIndex()

        if (index == 'prev' and currTable > 0):
            self.stackedTableLayout.setCurrentIndex(currTable - 1)
        elif (index == 'prev'):
            self.stackedTableLayout.setCurrentIndex(
                len(self.stackedTableLayout) - 1)

        if (index == 'next' and currTable < len(self.stackedTableLayout) - 1):
            self.stackedTableLayout.setCurrentIndex(currTable + 1)
        elif (index == 'next'):
            self.stackedTableLayout.setCurrentIndex(0)

        self.setTableNumberLabel()

    def setTableNumberLabel(self):
        self.tableNumberLabel.setText(
            f'Page: {self.stackedTableLayout.currentIndex() + 1} of {len(self.stackedTableLayout)}')
