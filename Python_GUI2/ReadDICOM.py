# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReadDICOM.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import shutil
import SimpleITK as sitk
import itk
import sys
import os
from DICOMtoHRD import DICOM_HRD
from registration import *


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
        self.line.setGeometry(QtCore.QRect(0, 180, 711, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 190, 701, 81))
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
        self.regsavepath=""
        self.ctsavepath=""
        self.fusionsavepath=""
        self.fusionresult=None
        
        self.currentpath=os.path.dirname(os.path.abspath(__file__))
        if (os.path.isdir('Cache')):
            shutil.rmtree('Cache')
        os.mkdir('Cache')
        self.cachepath=os.path.join(self.currentpath,"Cache","")

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

        self.Registrationbutton.setEnabled(False)
        self.Fusionbutton.setEnabled(False)

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

        if self.fnameCT!="" and self.fnameMRI!="":
            self.Registrationbutton.setEnabled(True)

    def openfolderMRI(self,MainWindow):
        self.fnameMRI = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        if self.fnameMRI!="":
            self.MRIfoldername.setText(self.fnameMRI)

            self.dicomfilesMRI = [name for name in os.listdir(self.fnameMRI) if name.endswith(".dcm")]
            self.dicomfilesMRI.sort()
            num_files=len(self.dicomfilesMRI)
            print(self.dicomfilesMRI)

        if self.fnameCT!="" and self.fnameMRI!="":
            self.Registrationbutton.setEnabled(True)

    def DicomtoHrd(self, MainWindow):

        MRIhdrid, MRIhrdsavepath = DICOM_HRD(self.fnameMRI, "hrdMRI", self.cachepath)
        CThdrid, CThrdsavepath = DICOM_HRD(self.fnameCT, "hrdCT", self.cachepath)
        self.label.setText("Reading "+MRIhdrid+"\nSaved to "+MRIhrdsavepath+"\n\nReading "+CThdrid+"\nSaved to "+CThrdsavepath)
        self.ctsavepath=CThrdsavepath

        return CThrdsavepath,MRIhrdsavepath


    def Registrationfunc(self, MainWindow):
        #print(self.comboBox.currentText())
        #print(self.comboBox.currentIndex())
        
        CThrdsavepath,MRIhrdsavepath = Ui_MainWindow.DicomtoHrd(self, MainWindow)
        
        if self.comboBox.currentIndex() == 0:
            regresult=Affine(CThrdsavepath,MRIhrdsavepath)
        elif self.comboBox.currentIndex() == 1:
            regresult=Bspline(CThrdsavepath,MRIhrdsavepath)
        elif self.comboBox.currentIndex() == 2:
            regresult=Both_AffineBspline(CThrdsavepath,MRIhrdsavepath)

        self.regsavepath= os.path.join(self.cachepath, 'final_registration.hdr')
        if os.path.exists(self.regsavepath):
            os.remove(self.regsavepath)
            os.remove(os.path.join(self.cachepath,'final_registration.img'))
        sitk.WriteImage(regresult, self.regsavepath)
        self.label.setText(self.comboBox.currentText()+" Registration complete\nSaved to "+self.regsavepath)
        self.Fusionbutton.setEnabled(True)


    def Fusionfunc(self, MainWindow):
        self.fusionresult=Fusion(self.ctsavepath,self.regsavepath)
        if os.path.exists(os.path.join(self.cachepath, 'final_fused.hdr')):
            os.remove(os.path.join(self.cachepath, 'final_fused.hdr'))
            os.remove(os.path.join(self.cachepath, 'final_fused.img'))
        sitk.WriteImage(self.fusionresult, os.path.join(self.cachepath, 'final_fused.hdr'))
        self.label.setText("Fusion complete\nSaved to "+self.regsavepath)
        

    def Savefunc(self, MainWindow):
        self.fnamesave = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        self.label.setText(self.fnamesave)
        sitk.WriteImage(self.fusionresult, os.path.join(self.fnamesave,"finalfusion.hdr"))
        self.label.setText("Image Saved")
        #reader = sitk.ImageSeriesReader()
        #dicom_names = reader.GetGDCMSeriesFileNames(self.fnameCT)
        #reader.SetFileNames(dicom_names)
        #image = reader.Execute()

        #writer = sitk.ImageFileWriter()
        #for i in range(image.GetDepth()):
            #image_slice = image[:, :, i]

            #writer.SetFileName(os.path.join(self.fnamesave, str(i) + '.dcm'))
            #writer.Execute(image_slice)



