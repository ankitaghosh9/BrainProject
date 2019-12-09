import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Window(QMainWindow):
   
   def __init__(self):
      super(Window,self).__init__()
      self.setGeometry(50,50,900,500)
      self.setWindowTitle("Template")
      self.menubarfunc()
      self.toolbarfunc()
      self.home()

 #to define menubar attributes     
   def menubarfunc(self):
      bar = self.menuBar()

      #FILE IN MENUBAR
      file = bar.addMenu("File")
      file.addAction("New")     
      save = QAction("Save",self)
      save.setShortcut("Ctrl+S")
      file.addAction(save)
      quit = QAction("Quit",self) 
      file.addAction(quit)

      #EDIT IN MENUBAR      
      edit = bar.addMenu("Edit")
      edit.addAction("copy")
      edit.addAction("paste")

      #TOOLS IN MENUBAR
      tools = bar.addMenu("Tools")
      tools.addAction("knife")
      tools.addAction("scalpel")
      tools.addAction("scissors")
      tools.addAction("tweezers")
      tools.addAction("forceps")

      #VIEW IN MENUBAR
      view = bar.addMenu("View")
      view.addAction("Axial")
      view.addAction("Sagittal")
      view.addAction("Coronal")
      
      bar.triggered[QAction].connect(self.mbtrigger)

#when menubar attributes are triggered          
   def mbtrigger(self,q):
      if q.text() == "Quit":
            sys.exit()
      elif q.text() == "knife":
            print "knife tool in use"
      else:
            print q.text()+" is triggered"

#to define toolbar attributes
   def toolbarfunc(self):
      tb = self.addToolBar("File")
            
      axial = QAction("Axial",self)
      tb.addAction(axial)            
      sagittal = QAction("Sagittal",self)
      tb.addAction(sagittal)
      coronal = QAction("Coronal",self)
      tb.addAction(coronal)
      tb.addSeparator()
      tb.addAction("knife")
      tb.addAction("scalpel")
      tb.addAction("scissors")
      tb.addAction("tweezers")
      tb.addAction("forceps")
      tb.addSeparator()

      tb.actionTriggered[QAction].connect(self.toolbtnpressed)

 #when bar attributes are triggered           
   def toolbtnpressed(self,a):
      print "pressed tool button is",a.text()
            

   def home(self):
      #reset button
      btn=QPushButton("Reset",self)
      btn.move(0,450)
      btn.clicked.connect(self.reset_application)

      #checkbox button1 and button2
      b1 = QCheckBox("Button1",self)
      b1.setChecked(True)
      b1.stateChanged.connect(lambda:self.btnstate(b1))
      b1.move(700,450)
      b2 = QCheckBox("Button2",self)
      b2.toggled.connect(lambda:self.btnstate(b2))
      b2.move(800,450)

      #drop down list
      cb = QComboBox(self)
      cb.addItems(["Cranium", "Cortex", "Cerebellum"])
      cb.activated[str].connect(self.selectionchange)
      cb.move(770,350)

      self.show()      

   def selectionchange(self,text):
      print "Current selection",text

   def btnstate(self,b):
      if b.text() == "Button1":
         if b.isChecked() == True:
            print b.text()+" is selected"
         else:
            print b.text()+" is deselected"
                        
      if b.text() == "Button2":
         if b.isChecked() == True:
            print b.text()+" is selected"
         else:
            print b.text()+" is deselected"
   
   def reset_application(self):
            choice = QMessageBox.question(self, 'Pop up window',
                  "reset to beginning?",
                  QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                  print("Reset done")
            else:
                  pass

def run():
      app=QApplication(sys.argv)
      GUI=Window()
      sys.exit(app.exec_())

run()

