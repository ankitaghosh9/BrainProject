# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReadDICOM.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import SimpleITK as sitk
import sys
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(712, 321)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MRI = QtWidgets.QLabel(self.centralwidget)
        self.MRI.setGeometry(QtCore.QRect(110, 30, 41, 21))
        self.MRI.setObjectName("MRI")
        self.CT = QtWidgets.QLabel(self.centralwidget)
        self.CT.setGeometry(QtCore.QRect(110, 60, 41, 21))
        self.CT.setObjectName("CT")
        self.MRIupload = QtWidgets.QPushButton(self.centralwidget)
        self.MRIupload.setGeometry(QtCore.QRect(10, 30, 89, 25))
        self.MRIupload.setObjectName("MRIupload")
        self.CTupload = QtWidgets.QPushButton(self.centralwidget)
        self.CTupload.setGeometry(QtCore.QRect(10, 60, 89, 25))
        self.CTupload.setObjectName("CTupload")
        self.MRIfoldername = QtWidgets.QLabel(self.centralwidget)
        self.MRIfoldername.setGeometry(QtCore.QRect(150, 30, 551, 17))
        self.MRIfoldername.setText("")
        self.MRIfoldername.setObjectName("MRIfoldername")
        self.CTfoldername = QtWidgets.QLabel(self.centralwidget)
        self.CTfoldername.setGeometry(QtCore.QRect(150, 60, 551, 17))
        self.CTfoldername.setText("")
        self.CTfoldername.setObjectName("CTfoldername")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 120, 86, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.Registrationbutton = QtWidgets.QPushButton(self.centralwidget)
        self.Registrationbutton.setGeometry(QtCore.QRect(20, 150, 89, 25))
        self.Registrationbutton.setObjectName("Registrationbutton")
        self.Fusionbutton = QtWidgets.QPushButton(self.centralwidget)
        self.Fusionbutton.setGeometry(QtCore.QRect(160, 120, 89, 51))
        self.Fusionbutton.setObjectName("Fusionbutton")
        self.Savebutton = QtWidgets.QPushButton(self.centralwidget)
        self.Savebutton.setGeometry(QtCore.QRect(590, 130, 89, 25))
        self.Savebutton.setObjectName("Savebutton")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 200, 711, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 220, 531, 31))
        self.label.setText("")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 712, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.fnameCT=""
        self.dicomfilesCT=[]
        self.fnameMRI=""
        self.dicomfilesMRI=[]
        self.fnamesave=""

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.MRI.setText(_translate("MainWindow", "MRI :"))
        self.CT.setText(_translate("MainWindow", " CT :"))
        self.MRIupload.setText(_translate("MainWindow", "Upload"))
        self.CTupload.setText(_translate("MainWindow", "Upload"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Affine"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Bspline"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Both"))
        self.Registrationbutton.setText(_translate("MainWindow", "Registration"))
        self.Fusionbutton.setText(_translate("MainWindow", "Fusion"))
        self.Savebutton.setText(_translate("MainWindow", "Save"))

        self.MRIupload.clicked.connect(self.openfolderMRI)
        self.CTupload.clicked.connect(self.openfolderCT)
        self.Registrationbutton.clicked.connect(self.Registrationfunc)
        self.Fusionbutton.clicked.connect(self.Fusionfunc)
        self.Savebutton.clicked.connect(self.Savefunc)


    def openfolderCT(self,MainWindow):
        self.fnameCT = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        if self.fnameCT!="":
            self.CTfoldername.setText(self.fnameCT)

            self.dicomfilesCT = [name for name in os.listdir(self.fnameCT) if name.endswith(".dcm")]
            self.dicomfilesCT.sort()
            num_files=len(self.dicomfilesCT)
            print(self.dicomfilesCT)

    def openfolderMRI(self,MainWindow):
        self.fnameMRI = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        if self.fnameMRI!="":
            self.MRIfoldername.setText(self.fnameMRI)

            self.dicomfilesMRI = [name for name in os.listdir(self.fnameMRI) if name.endswith(".dcm")]
            self.dicomfilesMRI.sort()
            num_files=len(self.dicomfilesMRI)
            print(self.dicomfilesMRI)

    def Registrationfunc(self, MainWindow):
        print(self.comboBox.currentText())
        print(self.comboBox.currentIndex())

    def Fusionfunc(self, MainWindow):
        print("inside fusion func")

    def Savefunc(self, MainWindow):
        self.fnamesave = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        self.label.setText(self.fnamesave)
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(self.fnameCT)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()

        writer = sitk.ImageFileWriter()
        for i in range(image.GetDepth()):
            image_slice = image[:, :, i]

            writer.SetFileName(os.path.join(self.fnamesave, str(i) + '.dcm'))
            writer.Execute(image_slice)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
