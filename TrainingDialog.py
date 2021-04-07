import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QDesktopWidget, qApp, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMenuBar, QPushButton, QLabel, QLineEdit, QFrame


class TrainingDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__()
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
        # Create widgets
        self.downloadButton = QPushButton("Download MNIST")
        self.trainButton = QPushButton("Train")
        self.cancelButton = QPushButton("Cancel")

        # Create layout and add widgets
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.downloadButton)
        self.buttonLayout.addWidget(self.trainButton)
        self.buttonLayout.addWidget(self.cancelButton)

    def createDialogLayout(self):
        # Create a main VBoxLayout
        self.mainVBoxLayout = QVBoxLayout()

        # Add our widget layouts to the mainVLayout
        self.mainVBoxLayout.addLayout(self.buttonLayout)

        # Add mainVLayout to this classes layout
        self.setLayout(self.mainVBoxLayout)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = TrainingDialog()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
