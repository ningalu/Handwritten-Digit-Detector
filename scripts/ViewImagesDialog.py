from __future__ import print_function
from math import ceil

import sys
from PyQt5.QtWidgets import QApplication, QWidget, qApp, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtWidgets import QPushButton, QTextEdit, QProgressBar, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

import time
import matplotlib.pyplot as plt
import numpy as np
import torchvision

from os import makedirs, path


class ViewImagesDialog(QDialog):

    def __init__(self, title, dataset):
        super().__init__()
        self.title = title
        self.dataset = dataset

        if ('train' in self.title.lower()):
            self.dirString = './images/train'
        else:
            self.dirString = './images/test'

        self.imageList = []
        self.createImageList()
        self.saveImages()

        self.imageLabel = 0
        self.viewImageIndex = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.createWidgetLayouts()
        self.createDialogLayout()

        self.centreWindow()
        self.show()

    def centreWindow(self):
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())
        # self.resize(320, 180)
        pass

    def createWidgetLayouts(self):
        # Create imageName and imageLabel (and set the default image to 1, 100)
        self.imageName = QLabel()
        self.imageName.setText('Data 1,100 (from left to right)')
        self.imageName.setAlignment(QtCore.Qt.AlignCenter)

        self.imageLabel = QLabel()
        pixmap = QPixmap(f'{self.dirString}/1,100.png')
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Create imageLayout and add the imageLabel and name to it
        self.imageLayout = QVBoxLayout()
        self.imageLayout.addWidget(self.imageLabel)
        self.imageLayout.addWidget(self.imageName)

        # Create the navigation buttons needed and put them in their own HBox
        self.previousButton = QPushButton('Previous')
        self.previousButton.clicked.connect(self.prevImage)
        self.nextButton = QPushButton('Next')
        self.nextButton.clicked.connect(self.nextImage)

        self.navLayout = QHBoxLayout()
        self.navLayout.addWidget(self.previousButton)
        self.navLayout.addWidget(self.nextButton)

        # Create the select image button
        self.selectButton = QPushButton('Select image')
        self.selectButton.clicked.connect(self.openImageFileDialog)

        # Create buttonLayout and add the buttons to it
        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.addLayout(self.navLayout)
        self.buttonLayout.addWidget(self.selectButton)

    def createDialogLayout(self):
        # Create a main HBoxLayout
        self.mainVBoxLayout = QVBoxLayout()

        # Add our widget layouts to the mainHLayout
        self.mainVBoxLayout.addLayout(self.imageLayout)
        self.mainVBoxLayout.addLayout(self.buttonLayout)

        # Add mainHLayout to this classes layout
        self.setLayout(self.mainVBoxLayout)

    def createImageList(self):
        for i in range(1, len(self.dataset)):
            # currImage is now a torch.Tensor
            currImage, _ = self.dataset[i]
            self.imageList.append(currImage)

    def saveImages(self):
        if not path.exists(self.dirString):
            makedirs(self.dirString)

        for i in range(0, 100):
            npImg = torchvision.utils.make_grid(
                self.imageList[(i * 100):(i * 100) + 100])
            npImg = npImg.numpy()
            npImg = np.transpose(npImg, (1, 2, 0))

            plt.imsave(
                f'{self.dirString}/{i*100 + 1},{(i*100) + 100}.png', npImg)

    def prevImage(self):
        if (self.viewImageIndex > 0):
            self.viewImageIndex -= 1
        else:
            self.viewImageIndex = 99

        self.setImage()

    def nextImage(self):
        if (self.viewImageIndex < 99):
            self.viewImageIndex += 1
        else:
            self.viewImageIndex = 0

        self.setImage()

    def setImage(self):
        pixmap = QPixmap(
            f'{self.dirString}/{self.viewImageIndex*100 + 1},{(self.viewImageIndex*100) + 100}.png')
        self.imageLabel.setPixmap(pixmap)

        self.imageName.setText(f'Data {self.viewImageIndex*100 + 1},{(self.viewImageIndex*100) + 100} (from left to right)')
        QApplication.processEvents()

    def openImageFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Select the image to be viewed", self.dirString, "PNG Files (*.png)", options=options)
        print(f'{fileName} selected')

        parsedFileName = fileName.split('/')
        parsedFileName = parsedFileName[-1].split(',')
        parsedFileName = parsedFileName[0]
        # print(parsedFileName)

        self.viewImageIndex = int((int(parsedFileName) - 1) / 100)
        # print(f'{self.viewImageIndex}')
        self.setImage()
