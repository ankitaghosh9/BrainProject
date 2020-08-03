# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReadDICOMSeriesQt.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!
import sys,fnmatch, os, glob
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
#from ReadDICOMSeriesfunctions import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_ReadDICOMSeriesQt(object):
    


    def setupUi(self, ReadDICOMSeriesQt):
        ReadDICOMSeriesQt.setObjectName(_fromUtf8("ReadDICOMSeriesQt"))
        ReadDICOMSeriesQt.resize(541, 531)
        self.centralWidget = QtGui.QWidget(ReadDICOMSeriesQt)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.buttonOpenFolder = QtGui.QPushButton(self.centralWidget)
        self.buttonOpenFolder.setGeometry(QtCore.QRect(10, 430, 121, 24))
        self.buttonOpenFolder.setObjectName(_fromUtf8("buttonOpenFolder"))
        self.sliderSlices = QtGui.QSlider(self.centralWidget)
        self.sliderSlices.setGeometry(QtCore.QRect(140, 430, 381, 23))
        self.sliderSlices.setOrientation(QtCore.Qt.Horizontal)
        self.sliderSlices.setObjectName(_fromUtf8("sliderSlices"))
        self.labelFolderName = QtGui.QLabel(self.centralWidget)
        self.labelFolderName.setGeometry(QtCore.QRect(140, 470, 381, 15))
        self.labelFolderName.setObjectName(_fromUtf8("labelFolderName"))
        self.labelSlicesNumber = QtGui.QLabel(self.centralWidget)
        self.labelSlicesNumber.setGeometry(QtCore.QRect(140, 500, 381, 15))
        self.labelSlicesNumber.setObjectName(_fromUtf8("labelSlicesNumber"))
        self.labelSlicesNumberTitle = QtGui.QLabel(self.centralWidget)
        self.labelSlicesNumberTitle.setGeometry(QtCore.QRect(20, 500, 59, 15))
        self.labelSlicesNumberTitle.setObjectName(_fromUtf8("labelSlicesNumberTitle"))
        self.labelFolderNameTitle = QtGui.QLabel(self.centralWidget)
        self.labelFolderNameTitle.setGeometry(QtCore.QRect(20, 470, 59, 15))
        self.labelFolderNameTitle.setObjectName(_fromUtf8("labelFolderNameTitle"))
        self.qvtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        self.qvtkWidget.setGeometry(QtCore.QRect(10, 10, 521, 411))
        self.qvtkWidget.setObjectName(_fromUtf8("qvtkWidget"))
        ReadDICOMSeriesQt.setCentralWidget(self.centralWidget)

        self.reader = vtk.vtkDICOMImageReader()
        self.imageViewer = vtk.vtkImageViewer()
        self.interactor = vtk.vtkInteractorStyleImage()
        self.renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        self.minSlice=0
        self.maxSlice=0
        self.fname=""
        self.dicomfiles=[]

        self.retranslateUi(ReadDICOMSeriesQt)
        QtCore.QMetaObject.connectSlotsByName(ReadDICOMSeriesQt)

    def retranslateUi(self, ReadDICOMSeriesQt):
        ReadDICOMSeriesQt.setWindowTitle(_translate("ReadDICOMSeriesQt", "DICOM Series", None))
        self.buttonOpenFolder.setText(_translate("ReadDICOMSeriesQt", "Open Folder", None))
        self.labelFolderName.setText(_translate("ReadDICOMSeriesQt", "-", None))
        self.labelSlicesNumber.setText(_translate("ReadDICOMSeriesQt", "-", None))
        self.labelSlicesNumberTitle.setText(_translate("ReadDICOMSeriesQt", "Slices:", None))
        self.labelFolderNameTitle.setText(_translate("ReadDICOMSeriesQt", "Folder:", None))

        self.buttonOpenFolder.clicked.connect(self.openfolder)
        self.sliderSlices.valueChanged.connect(self.valuechange)

    def openfolder(self,ReadDICOMSeriesQt):
        self.fname = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        self.labelFolderName.setText(_translate("ReadDICOMSeriesQt", self.fname, None))

        self.dicomfiles = [name for name in os.listdir(self.fname) if name.endswith(".dcm")]
        self.dicomfiles.sort()
        num_files=len(self.dicomfiles)
        print(self.dicomfiles)
        
        self.sliderSlices.setMinimum(1)
        self.sliderSlices.setMaximum(num_files)
        
        self.drawdicomseries(ReadDICOMSeriesQt, self.fname, 0)


    def drawdicomseries(self, ReadDICOMSeriesQt, ndicom, slicenum):
        

        #self.reader.SetDirectoryName(ndicom)
        print(self.dicomfiles[slicenum])
        self.reader.SetFileName(os.path.join(ndicom, self.dicomfiles[slicenum]))
        self.reader.Update()

        self.imageViewer.SetInputConnection(self.reader.GetOutputPort())

        self.qvtkWidget.SetRenderWindow(self.imageViewer.GetRenderWindow())

        #self.imageViewer.SetupInteractor(self.qvtkWidget.GetInteractor())
        self.renderWindowInteractor.SetInteractorStyle(self.interactor)
        self.imageViewer.SetupInteractor(self.renderWindowInteractor)

        self.imageViewer.Render()

        #num_files = len(glob.glob1(ndicom,"*.dcm"))

        #self.minSlice = self.imageViewer.GetSliceMin()
        #self.maxSlice = self.imageViewer.GetSliceMax()
    

    def valuechange(self,ReadDICOMSeriesQt):
        size =self.sliderSlices.value()
        self.labelSlicesNumber.setText(str(size))
        #self.imageViewer.SetSlice(size)
        #self.imageViewer.Render()
        self.drawdicomseries(ReadDICOMSeriesQt, self.fname, size-1)
