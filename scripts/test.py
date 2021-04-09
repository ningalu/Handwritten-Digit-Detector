# import time
# import matplotlib.pyplot as plt
# import numpy as np

# from torchvision import datasets, transforms

# dataset = datasets.MNIST(
#     root='./mnist_data',
#     download=True,
#     transform=transforms.ToTensor()
# )

# start = time.time()

# x, _ = dataset[7777] # x is now a torch.Tensor
# plt.imshow(x.numpy()[0], cmap='gray')

# end = time.time()
# print(f'it took {end - start} sec to load an image.')
# plt.show()

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel
# from PyQt5.QtGui import QIcon, QPixmap

# class App(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 image - pythonspot.com'
#         # self.left = 10
#         # self.top = 10
#         # self.width = 640
#         # self.height = 480
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         # self.setGeometry(self.left, self.top, self.width, self.height)

#         # Create widget
#         label = QLabel(self)
#         pixmap = QPixmap('image.png')
#         label.setPixmap(pixmap)
#         self.resize(pixmap.width(),pixmap.height())

#         self.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())

# import sys
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

# class MainWindow(QMainWindow):

#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.title = "Image Viewer"
#         self.setWindowTitle(self.title)

#         label = QLabel(self)
#         pixmap = QPixmap('image.png')
#         label.setPixmap(pixmap)
#         self.setCentralWidget(label)
#         self.resize(pixmap.width(), pixmap.height())


# app = QApplication(sys.argv)
# w = MainWindow()
# w.show()
# sys.exit(app.exec_())

from PyQt5 import QtWidgets, QtGui, QtCore

from matplotlib.pyplot import imread
import sys

app = QtWidgets.QApplication(sys.argv)

#input_image = imread('./images/train/1,100.png')
#pixmap01 = QtGui.QPixmap.fromImage('./images/train/1,100.png')
pixmap_image = QtGui.QPixmap('./images/train/1,100.png')
label_imageDisplay = QtWidgets.QLabel()
label_imageDisplay.setPixmap(pixmap_image)
# label_imageDisplay.setAlignment(QtCore.Qt.AlignCenter)
# label_imageDisplay.setScaledContents(True)
# label_imageDisplay.setMinimumSize(1,1)
label_imageDisplay.show()
sys.exit(app.exec_())