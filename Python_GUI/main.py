from ReadDICOMSeriesQt import *
import sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ReadDICOMSeriesQt = QtGui.QMainWindow()
    ui = Ui_ReadDICOMSeriesQt()
    ui.setupUi(ReadDICOMSeriesQt)
    ReadDICOMSeriesQt.show()
    sys.exit(app.exec_())

main()
