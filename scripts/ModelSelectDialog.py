from PyQt5.QtWidgets import QApplication, QWidget, qApp, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QPushButton, QComboBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

class ModelSelectDialog(QDialog):
    modelSelected = pyqtSignal(str)
    modelSelectedFlag = 0

    def __init__(self, appSelectedModel):
        super().__init__()
        self.appSelectedModel = appSelectedModel

        self.initUI()
        self.modelSelectedFlag = 1

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

        index = self.modelList.findText(self.appSelectedModel)
        if (index != -1 ):
            self.modelList.setCurrentIndex(index);

    def addWidgetsToWidgetLayouts(self):
        self.labelLayout.addWidget(self.modelListLabel)
        self.modelListLayout.addWidget(self.modelList)
    
    def createCentralLayout(self):
        grid = QGridLayout()

        grid.addLayout(self.labelLayout, 0, 0)
        grid.addLayout(self.modelListLayout, 1, 0)

        self.setLayout(grid)
    
    def emitModelPicked(self):
        modelPicked = ''

        if (self.modelList.currentText() == "None") :
            modelPicked = "None"
        elif (self.modelList.currentText() == "PyTorch"):
            modelPicked = "PyTorch"

        self.modelSelected.emit(modelPicked)

        if (self.modelSelectedFlag == 1):
            selectedDialog = QMessageBox()
            selectedDialog.setWindowTitle('New model selected')
            selectedDialog.setIcon(QMessageBox.NoIcon)
            selectedDialog.setText(f"The '{modelPicked}' model has been selected.")

            selectedDialog.exec_()

