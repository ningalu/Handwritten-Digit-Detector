from __future__ import print_function

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, qApp, QHBoxLayout, QVBoxLayout

from torch import nn, optim, cuda, save
from torch.utils import data
from torchvision import datasets, transforms
import torch.nn.functional as F
from math import ceil
import time

from os import makedirs, path

from Net import Net


class TrainingWorker(QObject):
    progressText = pyqtSignal(str, bool)
    progressBar = pyqtSignal(int)
    getModel = pyqtSignal(Net)
    finished = pyqtSignal()

    def run(self):
        self.flag = 1
        model = self.trainModel()

        self.getModel.emit(model)
        self.finished.emit()

    # Downloads both the train and test sets, but only one download=True needed so test omitted
    def loadMNIST(self):
        self.progressText.emit('', True)
        self.progressText.emit("Loading train dataset...", False)

        # MNIST Dataset
        self.train_dataset = datasets.MNIST(root='./mnist_data/',
                                            train=True,
                                            transform=transforms.ToTensor(),
                                            download=False)

        self.progressBar.emit(99)

        self.progressText.emit("Loading test dataset...", False)
        self.test_dataset = datasets.MNIST(root='./mnist_data/',
                                           train=False,
                                           transform=transforms.ToTensor())

        self.progressBar.emit(100)
        self.progressText.emit("MNIST Dataset successfully loaded.", False)
        self.progressBar.emit(0)

    def trainModel(self):
        # Training settings
        batch_size = 64
        device = 'cuda' if cuda.is_available() else 'cpu'
        print(f'Training MNIST Model on {device}\n{"=" * 44}')

        # MNIST Dataset
        self.loadMNIST()

        self.progressText.emit('', True)
        self.progressText.emit("Training...", False)

        # Data Loader (Input Pipeline)
        train_loader = data.DataLoader(dataset=self.train_dataset,
                                       batch_size=batch_size,
                                       shuffle=True)

        test_loader = data.DataLoader(dataset=self.test_dataset,
                                      batch_size=batch_size,
                                      shuffle=False)

        model = Net()
        model.to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

        def train(epoch):
            model.train()
            for batch_idx, (data, target) in enumerate(train_loader):
                if self.flag == 0:
                    break

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
                if self.flag == 0:
                    break

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

        if __name__ == 'TrainingWorker':
            overallAccuracy = 0.0

            since = time.time()
            for epoch in range(1, 10):
                if self.flag == 0:
                    break

                self.progressText.emit(f"Training Epoch: {epoch}", False)
                self.progressBar.emit(ceil((epoch - 1) * (100/9)))

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

            if (self.flag == 1):
                print(
                    f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {device}!')
            self.progressText.emit(
                f"Overall accuracy: {overallAccuracy:.0f}%", False)
            self.progressBar.emit(0)

            save(model.state_dict(), './mnist_model.zip')
            return model;

    def stop(self):
        self.flag = 0
        print("Training thread exited")
