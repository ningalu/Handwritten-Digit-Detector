from PyQt5.QtWidgets import QApplication, QWidget, qApp, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton, QComboBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

class ModelSelectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.model = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Select Model')
        self.centerWindow()

        self.createWidgetLayouts()
        self.createWidgets()
        self.addWidgetsToWidgetLayouts()
        self.createCentralLayout()

    def centerWindow(self):
        self.resize(320, 100)
    
    def createWidgetLayouts(self):
        self.labelLayout = QHBoxLayout()

        self.modelListLayout = QHBoxLayout()

    def createWidgets(self):
        self.modelListLabel = QLabel('Select the model to be used for recognition')

        self.modelList = QComboBox()
        self.modelList.addItem('None')
        self.modelList.addItem('PyTorch')
        self.modelList.currentIndexChanged.connect(self.emitModelPicked)

    def addWidgetsToWidgetLayouts(self):
        self.labelLayout.addWidget(self.modelListLabel)
        self.modelListLayout.addWidget(self.modelList)
    
    def createCentralLayout(self):
        grid = QGridLayout()

        grid.addLayout(self.labelLayout, 0, 0)
        grid.addLayout(self.modelListLayout, 1, 0)

        self.setLayout(grid)
    
    def emitModelPicked(self):
        pass

