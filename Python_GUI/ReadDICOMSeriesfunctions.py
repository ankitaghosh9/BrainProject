#from ReadDICOMSeriesQt import *
import sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

reader = vtk.vtkDICOMImageReader()
imageViewer = vtk.vtkImageViewer()

class ReadDICOMSeriesfunc():

	def openfolder(flabel):
		fname = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
		flabel.setText(_translate("ReadDICOMSeriesQt", fname, None))
		#drawdicomseries(fname)


	#def drawdicomseries(ndicom):
		#reader.SetDirectoryName(ndicom)
		#reader.Update()

		#imageViewer.SetInputConnection(reader.GetOutputPort())

		#ReadDICOMSeriesQt.qvtkWidget.SetRenderWindow(imageViewer.GetRenderWindow())

		#imageViewer.SetupInteractor(ReadDICOMSeriesQt.qvtkWidget.GetInteractor())

		#imageViewer.Render()





