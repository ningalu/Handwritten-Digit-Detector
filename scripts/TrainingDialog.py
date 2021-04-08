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


class TrainingDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.train_dataset = []
        self.test_dataset = []
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
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)

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
        self.progressBar.setValue(100)
        QApplication.processEvents()
        self.progressTextBox.append("MNIST Dataset successfully downloaded.")
        self.progressBar.setValue(0)

        # return train_dataset

    def trainModel(self):
        # Training settings
        batch_size = 64
        device = 'cuda' if cuda.is_available() else 'cpu'
        print(f'Training MNIST Model on {device}\n{"=" * 44}')

        # MNIST Dataset
        #self.train_dataset = self.downloadMNIST()
        self.downloadMNIST()

        self.test_dataset = datasets.MNIST(root='./mnist_data/',
                                           train=False,
                                           transform=transforms.ToTensor())

        self.progressTextBox.setText('')
        self.progressTextBox.append("Training...")

        # Data Loader (Input Pipeline)
        train_loader = data.DataLoader(dataset=self.train_dataset,
                                       batch_size=batch_size,
                                       shuffle=True)

        test_loader = data.DataLoader(dataset=self.test_dataset,
                                      batch_size=batch_size,
                                      shuffle=False)

        class Net(nn.Module):

            def __init__(self):
                super(Net, self).__init__()
                self.l1 = nn.Linear(784, 520)
                self.l2 = nn.Linear(520, 320)
                self.l3 = nn.Linear(320, 240)
                self.l4 = nn.Linear(240, 120)
                self.l5 = nn.Linear(120, 10)

            def forward(self, x):
                # Flatten the data (n, 1, 28, 28)-> (n, 784)
                x = x.view(-1, 784)
                x = F.relu(self.l1(x))
                x = F.relu(self.l2(x))
                x = F.relu(self.l3(x))
                x = F.relu(self.l4(x))
                return self.l5(x)

        model = Net()
        model.to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

        def train(epoch):
            model.train()
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(device), target.to(device)
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                if batch_idx % 10 == 0:
                    print('Train Epoch: {} | Batch Status: {}/{} ({:.0f}%) | Loss: {:.6f}'.format(
                        epoch, batch_idx *
                        len(data), len(train_loader.dataset),
                        100. * batch_idx / len(train_loader), loss.item()))

        def test():
            model.eval()
            test_loss = 0
            correct = 0

            accuracy = 0.0

            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                # sum up batch loss
                test_loss += criterion(output, target).item()
                # get the index of the max
                pred = output.data.max(1, keepdim=True)[1]
                correct += pred.eq(target.data.view_as(pred)).cpu().sum()

            test_loss /= len(test_loader.dataset)
            print(f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} '
                  f'({100. * correct / len(test_loader.dataset):.0f}%)')

            accuracy = 100 * correct/len(test_loader.dataset)
            return accuracy

        if __name__ == 'TrainingDialog':
            overallAccuracy = 0.0

            since = time.time()
            for epoch in range(1, 10):
                self.progressTextBox.append(f"Training Epoch: {epoch}")
                self.progressBar.setValue(ceil((epoch - 1) * (100/9)))
                # Needed for the GUI to update when the app stops responding
                QApplication.processEvents()

                epoch_start = time.time()
                train(epoch)
                m, s = divmod(time.time() - epoch_start, 60)
                print(f'Training time: {m:.0f}m {s:.0f}s')

                if (epoch == 9):
                    overallAccuracy = test()
                else:
                    test()

                m, s = divmod(time.time() - epoch_start, 60)
                print(f'Testing time: {m:.0f}m {s:.0f}s')

            m, s = divmod(time.time() - since, 60)

            print(
                f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {device}!')
            self.progressTextBox.append(
                f"Overall accuracy: {overallAccuracy:.0f}%")
            self.progressBar.setValue(0)

    def getTrainSet(self):

        return self.train_dataset

    def getTestSet(self):

        return self.test_dataset