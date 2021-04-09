from __future__ import print_function
from math import ceil

import sys
from PyQt5.QtWidgets import QApplication, QWidget, qApp, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton, QTextEdit, QProgressBar, QLabel
from PyQt5.QtGui import QIcon, QPixmap

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
        # Create imageLabel and set the default image to 1, 100
        self.imageLabel = QLabel()
        pixmap = QPixmap(f'{self.dirString}/1,100.png')
        self.imageLabel.setPixmap(pixmap)

        # Create imageLayout and add the imageLabel to it
        self.imageLayout = QVBoxLayout()
        self.imageLayout.addWidget(self.imageLabel)

        # Create the buttons needed
        self.previousButton = QPushButton('Previous')
        self.previousButton.clicked.connect(self.prevViewImage)
        self.nextButton = QPushButton('Next')
        self.nextButton.clicked.connect(self.nextViewImage)

        # selectButton = QPushButton('Select image')
        # menu = QMenu(self)
        # menu.addAction('First Item')
        # menu.addAction('Second Item')
        # menu.addAction('Third Item')
        # menu.addAction('Fourth Item')
        # popupbutton.setMenu(menu)

        # Create buttonLayout and add the buttons to it
        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.addWidget(self.previousButton)
        self.buttonLayout.addWidget(self.nextButton)
        # self.buttonLayout.addWidget(selectButton)

    def createDialogLayout(self):
        # Create a main HBoxLayout
        self.mainHBoxLayout = QHBoxLayout()

        # Add our widget layouts to the mainHLayout
        self.mainHBoxLayout.addLayout(self.imageLayout)
        self.mainHBoxLayout.addLayout(self.buttonLayout)

        # Add mainHLayout to this classes layout
        self.setLayout(self.mainHBoxLayout)

    def createImageList(self):
        for i in range(1, len(self.dataset)):
            # currImage is now a torch.Tensor
            currImage, _ = self.dataset[i]
            self.imageList.append(currImage)

    def saveImages(self):
        if not path.exists(self.dirString):
            makedirs(self.dirString)

        for i in range(0, 100):
            npimg = torchvision.utils.make_grid(
                self.imageList[(i * 100):(i * 100) + 100])
            npimg = npimg.numpy()
            npimg = np.transpose(npimg, (1, 2, 0))

            plt.imsave(
                f'{self.dirString}/{i*100 + 1},{(i*100) + 100}.png', npimg)

    def prevViewImage(self):
        if (self.viewImageIndex > 0):
            self.viewImageIndex -= 1
        else:
            self.viewImageIndex = 99

        pixmap = QPixmap(
            f'{self.dirString}/{self.viewImageIndex*100 + 1},{(self.viewImageIndex*100) + 100}.png')
        self.imageLabel.setPixmap(pixmap)
        QApplication.processEvents()

    def nextViewImage(self):
        if (self.viewImageIndex < 99):
            self.viewImageIndex += 1
        else:
            self.viewImageIndex = 0

        pixmap = QPixmap(
            f'{self.dirString}/{self.viewImageIndex*100 + 1},{(self.viewImageIndex*100) + 100}.png')
        self.imageLabel.setPixmap(pixmap)
        QApplication.processEvents()
