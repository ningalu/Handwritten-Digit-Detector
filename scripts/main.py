import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QDesktopWidget, qApp, QMenuBar


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.centreWindow()

    def initUI(self):
        self.setWindowTitle('Handwritten Digit Recognizer')
        self.centreWindow()
        self.createMenuBar()

        self.show()

    def centreWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.resize(640, 360)

    def createMenuBar(self):
        # -- Creation of Actions
        trainModelAct = QAction('&Train Model', self)
        #trainModelAct.triggered.connect()
        exitAct = QAction('&Quit', self)
        exitAct.triggered.connect(qApp.quit)

        viewTrainImgsAct = QAction('&View Training Images', self)
        #viewTrainImgsAct.triggered.connect()
        viewTestImgsAct = QAction('&View Testing Images', self)
        #viewTestImgsAct.triggered.connect()

        # -- Create MenuBar
        menubar = self.menuBar()

        # -- Add menus and actions to the MenuBar
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(trainModelAct)
        fileMenu.addAction(exitAct)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(viewTrainImgsAct)
        viewMenu.addAction(viewTestImgsAct)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   sys.exit(app.exec_())
