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

        self.imageList = []  # An array of image.numpy()[0]
        self.createImageList()
        # self.classes = ['0','1','2','3','4','5','6','7','8','9']

        self.initUI()

        self.saveImage(torchvision.utils.make_grid(self.imageList[0:100]))
        # print labels
        # print(' '.join('%5s' % self.classes[labels[j]] for j in range(64)))

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

    def saveImage(self, img):
        npimg = img.numpy()
        npimg = np.transpose(npimg, (1, 2, 0))
        # plt.imshow(np.transpose(npimg, (1, 2, 0)))

        if not path.exists('./images'):
            makedirs('./images')
        plt.imsave('./images/test_image.png', npimg)
