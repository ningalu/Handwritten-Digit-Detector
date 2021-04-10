from __future__ import print_function
from math import ceil

import sys
from PyQt5.QtWidgets import QApplication, QWidget, qApp, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton, QTextEdit, QProgressBar
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from torch import nn, optim, cuda
from torchvision import datasets, transforms
import time

from TrainingWorker import TrainingWorker


class TrainingDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.train_dataset = []
        self.test_dataset = []

        # trainingWorker created here to allow cancelButton to know what trainingWorker.stop refers to initially
        self.trainingWorker = TrainingWorker()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Model Training Options')
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
        # Create text box for progress text
        self.progressTextBox = QTextEdit()
        self.progressTextBox.setReadOnly(True)

        # Create text box layout and add widget
        self.progressTextLayout = QVBoxLayout()
        self.progressTextLayout.addWidget(self.progressTextBox)

        # Create progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)

        # Create bar layout and add widget
        self.progressBarLayout = QVBoxLayout()
        self.progressBarLayout.addWidget(self.progressBar)

        # Create buttons
        self.downloadButton = QPushButton("Download MNIST")
        self.downloadButton.clicked.connect(self.downloadMNIST)
        self.trainButton = QPushButton("Train")
        self.trainButton.clicked.connect(self.trainModel)
        # We should not be able to use the Train button until we have used Download at least once
        self.trainButton.setDisabled(True)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelButtonAction)

        # Create button layout and add widgets
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.downloadButton)
        self.buttonLayout.addWidget(self.trainButton)
        self.buttonLayout.addWidget(self.cancelButton)

    def createDialogLayout(self):
        # Create a main VBoxLayout
        self.mainVBoxLayout = QVBoxLayout()

        # Add our widget layouts to the mainVLayout
        self.mainVBoxLayout.addLayout(self.progressTextLayout)
        self.mainVBoxLayout.addLayout(self.progressBarLayout)
        self.mainVBoxLayout.addLayout(self.buttonLayout)

        # Add mainVLayout to this classes layout
        self.setLayout(self.mainVBoxLayout)

# Downloads both the train and test sets, but only one download=True needed so test omitted
    def downloadMNIST(self):
        self.progressTextBox.setText('')
        self.progressTextBox.append("Downloading train dataset...")
        # Needed for the GUI to update when the app stops responding
        QApplication.processEvents()

        # MNIST Dataset
        self.train_dataset = datasets.MNIST(root='./mnist_data/',
                                            train=True,
                                            transform=transforms.ToTensor(),
                                            download=True)

        self.progressBar.setValue(99)
        self.progressTextBox.append("Downloading test dataset...")
        QApplication.processEvents()
        self.test_dataset = datasets.MNIST(root='./mnist_data/',
                                           train=False,
                                           transform=transforms.ToTensor())
        self.progressBar.setValue(100)
        QApplication.processEvents()
        self.progressTextBox.append("MNIST Dataset successfully downloaded.")
        self.progressBar.setValue(0)

        # Once we click Download we should no longer be able to click Train
        self.trainButton.setDisabled(False)

    def trainModel(self):
        # Threading
        self.thread = QThread()

        # If we click Train we need to create a new worker, to begin the process again
        self.trainingWorker = TrainingWorker()

        self.trainingWorker.moveToThread(self.thread)

        self.thread.started.connect(self.trainingWorker.run)
        self.trainingWorker.finished.connect(self.thread.quit)
        self.trainingWorker.finished.connect(self.trainingWorker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        # Once the thread starts training we should no longer be able to Download or click Train
        self.trainButton.setDisabled(True)
        self.downloadButton.setDisabled(True)

    def cancelButtonAction(self):
        # If the cancel button is clicked, exit the thread and allow Train and Download to be clicked again
        self.trainingWorker.stop()
        self.trainButton.setDisabled(False)
        self.downloadButton.setDisabled(False)

    def getTrainSet(self):

        return self.train_dataset

    def getTestSet(self):

        return self.test_dataset
