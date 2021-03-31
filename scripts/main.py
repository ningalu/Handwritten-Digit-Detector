import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QDesktopWidget, qApp, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMenuBar, QPushButton, QLabel, QLineEdit, QFrame


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Handwritten Digit Recognizer')
        self.createMenuBar()
        self.createLayout()

        self.centreWindow()
        self.show()

    def centreWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.resize(480, 360)

    def createMenuBar(self):
        # Create Actions
        trainModelAct = QAction('&Train Model', self)
        #trainModelAct.triggered.connect()
        exitAct = QAction('&Quit', self)
        exitAct.triggered.connect(qApp.quit)

        viewTrainImgsAct = QAction('&View Training Images', self)
        #viewTrainImgsAct.triggered.connect()
        viewTestImgsAct = QAction('&View Testing Images', self)
        #viewTestImgsAct.triggered.connect()

        # Create MenuBar
        menubar = self.menuBar()

        # Add menus and actions to the MenuBar
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(trainModelAct)
        fileMenu.addAction(exitAct)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(viewTrainImgsAct)
        viewMenu.addAction(viewTestImgsAct)

    def createLayout(self):
        # Create a central QWidget that can be displayed in QMainWindow
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create a Grid Layout where we will assign our two box layouts
        grid = QGridLayout()
        leftBox = QVBoxLayout()
        rightBox = QVBoxLayout()

        # -- Creating Left Side of Layout
        # Create a layout for the drawing canvas
        canvasLayout = QVBoxLayout()
        # Add widgets
        self.canvas = QFrame(self)
        self.canvas.setGeometry(150, 20, 100, 100)
        self.canvas.setStyleSheet(
            "QWidget { border: 2px solid cornflowerblue; background-color: white;}")
        canvasLayout.addWidget(self.canvas)

        # Add required layouts to leftBox
        leftBox.addLayout(canvasLayout)

        # -- Creating Right Side of Layout
        # Create buttonLayout (a vbox) and assign four buttons to it
        buttonLayout = QVBoxLayout()
        # Add all required buttons to the box
        buttonLayout.setSpacing(0)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.addWidget(QPushButton('Clear'))
        buttonLayout.addWidget(QPushButton('Random'))
        buttonLayout.addWidget(QPushButton('Model'))
        buttonLayout.addWidget(QPushButton('Recognize'))

        # Create a layout for the class probability display
        classProbLayout = QVBoxLayout()
        # Add widgets
        classProbLayout.addWidget(QLabel('Class Probability'))
        classProbLayout.addWidget(QLineEdit('Graph of class probability'))
        classProbLayout.addWidget(QLineEdit('Class detected'))

        # Add required layouts to rightBox
        rightBox.addLayout(buttonLayout)
        rightBox.addLayout(classProbLayout)

        # Add left and right boxes (containing our widget layouts) to grid
        grid.addLayout(leftBox, 0, 0)
        grid.addLayout(rightBox, 0, 1)

        # Resize columns of grid
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)

        #Set central widget's layout to our grid
        self.centralWidget.setLayout(grid)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   sys.exit(app.exec_())
