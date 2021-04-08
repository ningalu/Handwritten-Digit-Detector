from __future__ import print_function
from math import ceil

import sys
from PyQt5.QtWidgets import QApplication, QWidget, qApp, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton, QTextEdit, QProgressBar

from torch import nn, optim, cuda
from torch.utils import data
from torchvision import datasets, transforms
import torch.nn.functional as F
import time


class ViewImagesDialog(QDialog):

    def __init__(self, title, dataset):
        super().__init__()
        self.title = title
        self.dataset = dataset

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
        # Create a main VBoxLayout
        self.mainHBoxLayout = QHBoxLayout()

        # Add our widget layouts to the mainVLayout

        # Add mainVLayout to this classes layout
        self.setLayout(self.mainHBoxLayout)
