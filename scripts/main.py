import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QDesktopWidget, qApp, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMenuBar, QPushButton, QLabel, QLineEdit, QFrame
from PyQt5.QtWidgets import QMessageBox

from TrainingDialog import TrainingDialog
from ViewImagesDialog import ViewImagesDialog


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.trainingDialog = 0
        self.viewTrainImagesDialog = 0
        self.viewTestImagesDialog = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Handwritten Digit Recognizer')
        self.createMenuBar()
        self.createWidgetLayouts()
        self.createCentralLayout()

        self.centreWindow()
        self.show()

    def centreWindow(self):
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())
        self.resize(720, 540)

    def createMenuBar(self):
        # Create Actions
        trainModelAct = QAction('&Train Model', self)
        trainModelAct.triggered.connect(self.showTrainingDialog)
        exitAct = QAction('&Quit', self)
        exitAct.triggered.connect(qApp.quit)

        viewTrainImgsAct = QAction('&View Training Images', self)
        viewTrainImgsAct.triggered.connect(self.showTrainImagesDialog)
        viewTestImgsAct = QAction('&View Testing Images', self)
        viewTestImgsAct.triggered.connect(self.showTestImagesDialog)

        # Create MenuBar
        menubar = self.menuBar()

        # Add menus and actions to the MenuBar
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(trainModelAct)
        fileMenu.addAction(exitAct)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(viewTrainImgsAct)
        viewMenu.addAction(viewTestImgsAct)

    def createCentralLayout(self):
        # Create a central QWidget that can be displayed in QMainWindow
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create a Grid Layout where we will assign our two box layouts
        grid = QGridLayout()
        leftBox = QVBoxLayout()
        rightBox = QVBoxLayout()

        # Add required widget layouts to leftBox
        leftBox.addLayout(self.canvasLayout)

        # Add required widget layouts to rightBox
        rightBox.addLayout(self.buttonLayout)
        rightBox.addLayout(self.classProbLayout)

        # Add left and right boxes (containing our widget layouts) to grid
        grid.addLayout(leftBox, 0, 0)
        grid.addLayout(rightBox, 0, 1)

        # Resize columns of grid
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)

        #Set central widget's layout to our grid
        self.centralWidget.setLayout(grid)

    def createWidgetLayouts(self):
        # -- Creating Left Side of Layout
        # Create a box layout for the canvas
        self.canvasLayout = QVBoxLayout()
        # Create canvas widget
        self.canvas = QFrame(self)
        self.canvas.setStyleSheet(
            "QWidget { border: 2px solid cornflowerblue; background-color: white;}")
        # Add canvas widget to canvas layout
        self.canvasLayout.addWidget(self.canvas)

        # -- Creating Right Side of Layout
        # Create a buttonLayout (a vbox)
        self.buttonLayout = QVBoxLayout()
        # Style buttons
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        # Add buttons to the box
        self.buttonLayout.addWidget(QPushButton('Clear'))
        self.buttonLayout.addWidget(QPushButton('Random'))
        self.buttonLayout.addWidget(QPushButton('Model'))
        self.buttonLayout.addWidget(QPushButton('Recognize'))

        # Create a layout for the class probability display
        self.classProbLayout = QVBoxLayout()
        # Add widgets to the box
        self.classProbLayout.addWidget(QLabel('Class Probability'))
        self.classProbLayout.addWidget(QLineEdit('Graph of class probability'))
        self.classProbLayout.addWidget(QLineEdit('Class detected'))

    def showTrainingDialog(self):
        self.trainingDialog = TrainingDialog()
        self.trainingDialog.exec_()

    def showTrainImagesDialog(self):
        try:  # Check if the dataset has been acquired by the trainingDialog yet
            self.train_dataset = self.trainingDialog.getTrainSet()

            if len(self.train_dataset) == 0:
                raise AttributeError
        except AttributeError:  # If not let the user know they have to get the dataset before viewing images
            dataMissingDialog = QMessageBox()
            dataMissingDialog.setWindowTitle('Data Missing')
            dataMissingDialog.setIcon(QMessageBox.Critical)
            dataMissingDialog.setText("The training dataset is missing.")
            dataMissingDialog.setInformativeText(
                "Make sure you go to File > Train Model and click 'Download MNIST' first.")

            dataMissingDialog.exec_()
        else:  # Otherwise create and execute the trainImagesDialog
            self.viewTrainImagesDialog = ViewImagesDialog(
                'View Training Images', self.train_dataset)
            self.viewTrainImagesDialog.exec_()

    def showTestImagesDialog(self):
        try:  # Check if the dataset has been acquired by the trainingDialog yet
            self.test_dataset = self.trainingDialog.getTestSet()

            if len(self.test_dataset) == 0:
                raise AttributeError
        except AttributeError:  # If not let the user know they have to get the dataset before viewing images
            dataMissingDialog = QMessageBox()
            dataMissingDialog.setWindowTitle('Data Missing')
            dataMissingDialog.setIcon(QMessageBox.Critical)
            dataMissingDialog.setText("The test dataset is missing.")
            dataMissingDialog.setInformativeText(
                "Make sure you go to File > Train Model and click 'Download MNIST' first.")

            dataMissingDialog.exec_()
        else:  # Otherwise create and execute the trainImagesDialog
            self.viewTrainImagesDialog = ViewImagesDialog(
                'View Test Images', self.test_dataset)
            self.viewTrainImagesDialog.exec_()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   sys.exit(app.exec_())
