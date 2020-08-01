import os
import sys
sys.path.insert(0, r"C:\Python27\Lib\site-packages")
from PyQt4 import QtCore, QtGui, uic


class Broken_Links_Form(QtGui.QMainWindow):
    def __init__(self, parent=QtGui.QApplication.instance()):
        super(Broken_Links_Form, self).__init__()
        uic.loadUi(
            r"C:\Users\anike\Documents\GitHub\FileDependenciesBrokenLinks\BrokenLinksJSONCompare\BrokenLinks.ui", self)
        self.toolButton_MayaLocation.clicked.connect(
            lambda: self.lineEdit_MayaLocation.setText(QtGui.QFileDialog.getOpenFileName()))
        self.toolButton_JSONLocation.clicked.connect(
            lambda: self.lineEdit_JSONLocation.setText(QtGui.QFileDialog.getOpenFileName()))
        self.mayaLocation = self.lineEdit_MayaLocation.textChanged[str].connect(self.validPath)
        self.jsonLocation = self.lineEdit_JSONLocation.textChanged[str].connect(self.validPath)
        self.pushButton_AnalyzeBrokenLinks.clicked.connect(
            lambda: self.findMissingLinks())

    def validPath(self, filePath=None):
        if os.path.isfile(filePath):
            return filePath

    def findMissingLinks(self):
        print(self.jsonLocation)
        shotNumber = openMaya(self.jsonLocation)
        textEdit_missingLinks.setText(checkItemInShot(
            jsonData == jsonData, shotNumber=shotNumber))

def main():
    
    app = QtGui.QApplication(sys.argv)
    Form = Broken_Links_Form()
    Form.show()
    sys.exit(app.exec_())

main()

