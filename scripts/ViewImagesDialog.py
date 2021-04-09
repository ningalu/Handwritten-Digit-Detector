from __future__ import print_function
from math import ceil

import sys
from PyQt5.QtWidgets import QApplication, QWidget, qApp, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton, QTextEdit, QProgressBar

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

        self.imageList = []
        self.createImageList()
        self.saveImages()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.createWidgetLayouts()
        self.createDialogLayout()

        self.centreWindow()

    def centreWindow(self):
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())
        self.resize(320, 180)

    def createWidgetLayouts(self):
        pass

    def createDialogLayout(self):
        # Create a main HBoxLayout
        self.mainHBoxLayout = QHBoxLayout()

        # Add our widget layouts to the mainHLayout

        # Add mainHLayout to this classes layout
        self.setLayout(self.mainHBoxLayout)

    def createImageList(self):
        for i in range(1, len(self.dataset)):
            # currImage is now a torch.Tensor
            currImage, _ = self.dataset[i]
            self.imageList.append(currImage)

        # plt.imshow(self.imageList[1], cmap='gray')
        # plt.show()

    def saveImages(self):
        if ('train' in self.title.lower()):
            dirString = './images/train'
        else:
            dirString = './images/test'

        if not path.exists(dirString):
            makedirs(dirString)

        for i in range(0, 100):
            npimg = torchvision.utils.make_grid(
                self.imageList[(i * 100):(i * 100) + 100])
            npimg = npimg.numpy()
            npimg = np.transpose(npimg, (1, 2, 0))

            plt.imsave(f'{dirString}/{i*100},{(i*100) + 100}.png', npimg)
            # plt.imshow(np.transpose(npimg, (1, 2, 0)))
